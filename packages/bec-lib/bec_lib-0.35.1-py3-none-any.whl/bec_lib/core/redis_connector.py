import enum
import time
import warnings
from functools import wraps

import redis

from .BECMessage import AlarmMessage, LogMessage
from .connector import (
    ConnectorBase,
    ConsumerConnector,
    ConsumerConnectorThreaded,
    MessageObject,
    ProducerConnector,
)
from .endpoints import MessageEndpoints


class Alarms(int, enum.Enum):
    WARNING = 0
    MINOR = 1
    MAJOR = 2


def catch_connection_error(func):
    """catch connection errors"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except redis.exceptions.ConnectionError:
            warnings.warn("Failed to connect to redis. Is the server running?")
            return None

    return wrapper


def trim_topic(topic: str, suffix: str) -> str:
    """
    trim topic to remove suffix

    Args:
        topic (str): topic to trim
        suffix (str): suffix to remove
    """
    if topic.endswith(suffix):
        return topic[: -len(suffix)]
    return topic


class RedisConnector(ConnectorBase):
    def __init__(self, bootstrap: list, redis_cls=None):
        super().__init__(bootstrap)
        self.redis_cls = redis_cls
        self.host, self.port = (
            bootstrap[0].split(":") if isinstance(bootstrap, list) else bootstrap.split(":")
        )
        self._notifications_producer = RedisProducer(
            host=self.host, port=self.port, redis_cls=self.redis_cls
        )

    def producer(self, **kwargs):
        return RedisProducer(host=self.host, port=self.port, redis_cls=self.redis_cls)

    # pylint: disable=too-many-arguments
    def consumer(
        self,
        topics=None,
        pattern=None,
        group_id=None,
        event=None,
        cb=None,
        threaded=True,
        name=None,
        **kwargs,
    ):
        if cb is None:
            raise ValueError("The callback function must be specified.")

        if threaded:
            if topics is None and pattern is None:
                raise ValueError("Topics must be set for threaded consumer")
            listener = RedisConsumerThreaded(
                self.host,
                self.port,
                topics,
                pattern,
                group_id,
                event,
                cb,
                redis_cls=self.redis_cls,
                name=name,
                **kwargs,
            )
            self._threads.append(listener)
            return listener
        return RedisConsumer(
            self.host,
            self.port,
            topics,
            pattern,
            group_id,
            event,
            cb,
            redis_cls=self.redis_cls,
            **kwargs,
        )

    def stream_consumer(
        self,
        topics=None,
        pattern=None,
        group_id=None,
        event=None,
        cb=None,
        from_start=False,
        newest_only=False,
        **kwargs,
    ):
        """
        Threaded stream consumer for redis streams.

        Args:
            topics (str, list): topics to subscribe to
            pattern (str, list): pattern to subscribe to
            group_id (str): group id
            event (threading.Event): event to stop the consumer
            cb (function): callback function
            from_start (bool): read from start. Defaults to False.
            newest_only (bool): read only the newest message. Defaults to False.
        """
        if cb is None:
            raise ValueError("The callback function must be specified.")

        if pattern:
            raise ValueError("Pattern is currently not supported for stream consumer.")

        if topics is None and pattern is None:
            raise ValueError("Topics must be set for stream consumer.")
        listener = RedisStreamConsumerThreaded(
            self.host,
            self.port,
            topics,
            pattern,
            group_id,
            event,
            cb,
            redis_cls=self.redis_cls,
            from_start=from_start,
            newest_only=newest_only,
            **kwargs,
        )
        self._threads.append(listener)
        return listener

    @catch_connection_error
    def log_warning(self, msg):
        """send a warning"""
        self._notifications_producer.send(
            MessageEndpoints.log(), LogMessage(log_type="warning", content=msg).dumps()
        )

    @catch_connection_error
    def log_message(self, msg):
        """send a log message"""
        self._notifications_producer.send(
            MessageEndpoints.log(), LogMessage(log_type="log", content=msg).dumps()
        )

    @catch_connection_error
    def log_error(self, msg):
        """send an error as log"""
        self._notifications_producer.send(
            MessageEndpoints.log(), LogMessage(log_type="error", content=msg).dumps()
        )

    @catch_connection_error
    def raise_alarm(
        self,
        severity: Alarms,
        alarm_type: str,
        source: str,
        content: dict,
        metadata: dict,
    ):
        """raise an alarm"""
        self._notifications_producer.set_and_publish(
            MessageEndpoints.alarm(),
            AlarmMessage(
                severity=severity,
                alarm_type=alarm_type,
                source=source,
                content=content,
                metadata=metadata,
            ).dumps(),
        )


class RedisProducer(ProducerConnector):
    def __init__(self, host: str, port: int, redis_cls=None) -> None:
        # pylint: disable=invalid-name
        if redis_cls:
            self.r = redis_cls(host=host, port=port)
            return
        self.r = redis.Redis(host=host, port=port)
        self.stream_keys = {}

    @catch_connection_error
    def send(self, topic: str, msg, pipe=None) -> None:
        """send to redis"""
        topic = trim_topic(topic, ":sub")
        client = pipe if pipe is not None else self.r
        client.publish(f"{topic}:sub", msg)

    @catch_connection_error
    def lpush(
        self, topic: str, msgs: str, pipe=None, max_size: int = None, expire: int = None
    ) -> None:
        """Time complexity: O(1) for each element added, so O(N) to
        add N elements when the command is called with multiple arguments.
        Insert all the specified values at the head of the list stored at key.
        If key does not exist, it is created as empty list before
        performing the push operations. When key holds a value that
        is not a list, an error is returned."""
        topic = trim_topic(topic, ":val")
        client = pipe if pipe is not None else self.pipeline()
        client.lpush(f"{topic}:val", msgs)
        if max_size:
            client.ltrim(f"{topic}:val", 0, max_size)
        if expire:
            client.expire(f"{topic}:val", expire)
        if not pipe:
            client.execute()

    @catch_connection_error
    def lset(self, topic: str, index: int, msgs: str, pipe=None) -> None:
        topic = trim_topic(topic, ":val")
        client = pipe if pipe is not None else self.r
        return client.lset(f"{topic}:val", index, msgs)

    @catch_connection_error
    def rpush(self, topic: str, msgs: str, pipe=None) -> int:
        """O(1) for each element added, so O(N) to add N elements when the
        command is called with multiple arguments. Insert all the specified
        values at the tail of the list stored at key. If key does not exist,
        it is created as empty list before performing the push operation. When
        key holds a value that is not a list, an error is returned."""
        topic = trim_topic(topic, ":val")
        client = pipe if pipe is not None else self.r
        return client.rpush(f"{topic}:val", msgs)

    @catch_connection_error
    def lrange(self, topic: str, start: int, end: int, pipe=None):
        """O(S+N) where S is the distance of start offset from HEAD for small
        lists, from nearest end (HEAD or TAIL) for large lists; and N is the
        number of elements in the specified range. Returns the specified elements
        of the list stored at key. The offsets start and stop are zero-based indexes,
        with 0 being the first element of the list (the head of the list), 1 being
        the next element and so on."""
        topic = trim_topic(topic, ":val")
        client = pipe if pipe is not None else self.r
        return client.lrange(f"{topic}:val", start, end)

    @catch_connection_error
    def set_and_publish(self, topic: str, msg, pipe=None, expire: int = None) -> None:
        """piped combination of self.publish and self.set"""
        topic = trim_topic(topic, ":val")
        topic = trim_topic(topic, ":sub")
        client = pipe if pipe is not None else self.pipeline()
        client.publish(f"{topic}:sub", msg)
        client.set(f"{topic}:val", msg)
        if expire:
            client.expire(f"{topic}:val", expire)
        if not pipe:
            client.execute()

    @catch_connection_error
    def set(self, topic: str, msg, pipe=None, is_dict=False, expire: int = None) -> None:
        """set redis value"""
        topic = trim_topic(topic, ":val")
        client = pipe if pipe is not None else self.pipeline()
        if is_dict:
            client.hmset(f"{topic}:val", msg)
        else:
            client.set(f"{topic}:val", msg)
        if expire:
            client.expire(f"{topic}:val", expire)
        if not pipe:
            client.execute()

    @catch_connection_error
    def keys(self, pattern: str) -> list:
        """returns all keys matching a pattern"""
        return self.r.keys(pattern)

    @catch_connection_error
    def pipeline(self):
        """create a new pipeline"""
        return self.r.pipeline()

    @catch_connection_error
    def delete(self, topic, pipe=None):
        """delete topic"""
        client = pipe if pipe is not None else self.r
        client.delete(topic)

    @catch_connection_error
    def get(self, topic: str, pipe=None, is_dict=False):
        """retrieve entry, either via hgetall or get"""
        topic = trim_topic(topic, ":val")
        client = pipe if pipe is not None else self.r
        if is_dict:
            return client.hgetall(f"{topic}:val")
        return client.get(f"{topic}:val")

    @catch_connection_error
    def xadd(self, topic: str, msg: dict, max_size=None, pipe=None, expire: int = None):
        """
        add to stream

        Args:
            topic (str): redis topic
            msg (dict): message to add
            max_size (int, optional): max size of stream. Defaults to None.
            pipe (Pipeline, optional): redis pipe. Defaults to None.
            expire (int, optional): expire time. Defaults to None.

        Examples:
            >>> redis.xadd("test", {"test": "test"})
            >>> redis.xadd("test", {"test": "test"}, max_size=10)
        """
        topic = trim_topic(topic, ":stream")
        if pipe:
            client = pipe
        elif expire:
            client = self.pipeline()
        else:
            client = self.r

        if max_size:
            client.xadd(f"{topic}:stream", msg, maxlen=max_size)
        else:
            client.xadd(f"{topic}:stream", msg)
        if expire:
            client.expire(f"{topic}:stream", expire)
        if not pipe and expire:
            client.execute()

    @catch_connection_error
    def get_last(self, topic: str, pipe=None, key=b"data"):
        """retrieve last entry from stream"""
        topic = trim_topic(topic, ":stream")
        client = pipe if pipe is not None else self.r
        msg = client.xrevrange(f"{topic}:stream", "+", "-", count=1)
        if not msg:
            return None
        if key is None:
            return msg[0][1]
        return msg[0][1].get(key)

    @catch_connection_error
    def xread(
        self,
        topic: str,
        id: str = None,
        count: int = None,
        block: int = None,
        pipe=None,
        from_start=False,
    ) -> list:
        """
        read from stream

        Args:
            topic (str): redis topic
            id (str, optional): id to read from. Defaults to None.
            count (int, optional): number of messages to read. Defaults to None.
            block (int, optional): block for x milliseconds. Defaults to None.
            pipe (Pipeline, optional): redis pipe. Defaults to None.
            from_start (bool, optional): read from start. Defaults to False.

        Returns:
            [list]: list of messages

        Examples:
            >>> redis.xread("test", "0-0")
            >>> redis.xread("test", "0-0", count=1)

            # read one message at a time
            >>> key = 0
            >>> msg = redis.xread("test", key, count=1)
            >>> key = msg[0][1][0][0]
            >>> next_msg = redis.xread("test", key, count=1)
        """
        client = pipe if pipe is not None else self.r
        if topic not in self.stream_keys:
            if from_start:
                self.stream_keys[topic] = "0-0"
            else:
                try:
                    self.stream_keys[topic] = client.xinfo_stream(f"{topic}:stream")[
                        "last-generated-id"
                    ]
                except redis.exceptions.ResponseError:
                    self.stream_keys[topic] = "0-0"
        if id is None:
            id = self.stream_keys[topic]

        msg = client.xread({f"{topic}:stream": id}, count=count, block=block)
        if msg:
            self.stream_keys[topic] = msg[0][1][-1][0]
        return msg

    @catch_connection_error
    def xrange(self, topic: str, min: str, max: str, count: int = None, pipe=None):
        """
        read a range from stream

        Args:
            topic (str): redis topic
            min (str): min id. Use "-" to read from start
            max (str): max id. Use "+" to read to end
            count (int, optional): number of messages to read. Defaults to None.
            pipe (Pipeline, optional): redis pipe. Defaults to None.
        """
        client = pipe if pipe is not None else self.r
        topic = trim_topic(topic, ":stream")
        return client.xrange(f"{topic}:stream", min, max, count=count)


class RedisConsumerMixin:
    def _init_topics_and_pattern(self, topics, pattern):
        if topics:
            if isinstance(topics, list):
                topics = [f"{topic}:sub" for topic in topics]
            else:
                topics = [f"{topics}:sub"]
        if pattern:
            if isinstance(pattern, list):
                pattern = [f"{pat}:sub" for pat in pattern]
            else:
                pattern = [f"{pattern}:sub"]
        return topics, pattern

    def _init_redis_cls(self, redis_cls):
        # pylint: disable=invalid-name
        if redis_cls:
            self.r = redis_cls(host=self.host, port=self.port)
        else:
            self.r = redis.Redis(host=self.host, port=self.port)

    @catch_connection_error
    def initialize_connector(self) -> None:
        if self.pattern is not None:
            self.pubsub.psubscribe(self.pattern)
        else:
            self.pubsub.subscribe(self.topics)


class RedisConsumer(RedisConsumerMixin, ConsumerConnector):
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        host,
        port,
        topics=None,
        pattern=None,
        group_id=None,
        event=None,
        cb=None,
        redis_cls=None,
        **kwargs,
    ):
        self.host = host
        self.port = port

        bootstrap_server = "".join([host, ":", port])
        topics, pattern = self._init_topics_and_pattern(topics, pattern)
        super().__init__(
            bootstrap_server=bootstrap_server,
            topics=topics,
            pattern=pattern,
            group_id=group_id,
            event=event,
            cb=cb,
            **kwargs,
        )
        self.error_message_sent = False
        self._init_redis_cls(redis_cls)
        self.pubsub = self.r.pubsub()
        self.initialize_connector()

    @catch_connection_error
    def poll_messages(self) -> None:
        """
        Poll messages from self.connector and call the callback function self.cb

        """
        messages = self.pubsub.get_message(ignore_subscribe_messages=True)
        if messages is not None:
            msg = MessageObject(topic=messages["channel"], value=messages["data"])
            return self.cb(msg, **self.kwargs)

        time.sleep(0.01)
        return None

    def shutdown(self):
        """shutdown the consumer"""
        self.pubsub.close()


class RedisStreamConsumerThreaded(RedisConsumerMixin, ConsumerConnectorThreaded):
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        host,
        port,
        topics=None,
        pattern=None,
        group_id=None,
        event=None,
        cb=None,
        redis_cls=None,
        from_start=False,
        newest_only=False,
        **kwargs,
    ):
        self.host = host
        self.port = port
        self.from_start = from_start
        self.newest_only = newest_only

        bootstrap_server = "".join([host, ":", port])
        topics, pattern = self._init_topics_and_pattern(topics, pattern)
        super().__init__(
            bootstrap_server=bootstrap_server,
            topics=topics,
            pattern=pattern,
            group_id=group_id,
            event=event,
            cb=cb,
            **kwargs,
        )

        self._init_redis_cls(redis_cls)

        self.sleep_times = [0.005, 0.1]
        self.last_received_msg = 0
        self.idle_time = 30
        self.error_message_sent = False
        self.stream_keys = {}

    def initialize_connector(self) -> None:
        pass

    def _init_topics_and_pattern(self, topics, pattern):
        if topics:
            if isinstance(topics, list):
                topics = [f"{trim_topic(topic, ':stream')}:stream" for topic in topics]
            else:
                topics = [f"{trim_topic(topics, ':stream')}:stream"]
        if pattern:
            if isinstance(pattern, list):
                pattern = [f"{trim_topic(pat, ':stream')}:stream" for pat in pattern]
            else:
                pattern = [f"{trim_topic(pattern, ':stream')}:stream"]
        return topics, pattern

    def get_id(self, topic: str) -> str:
        """
        Get the stream key for the given topic.

        Args:
            topic (str): topic to get the stream key for
        """
        if topic not in self.stream_keys:
            return "0-0"
        return self.stream_keys.get(topic)

    def get_newest_message(self, container: list, append=True) -> None:
        """
        Get the newest message from the stream and update the stream key. If
        append is True, append the message to the container.

        Args:
            container (list): container to append the message to
            append (bool, optional): append to container. Defaults to True.
        """
        for topic in self.topics:
            msg = self.r.xrevrange(topic, "+", "-", count=1)
            if msg:
                if append:
                    container.append((topic, msg[0][1]))
                self.stream_keys[topic] = msg[0][0]
            else:
                self.stream_keys[topic] = "0-0"

    @catch_connection_error
    def poll_messages(self) -> None:
        """
        Poll messages from self.connector and call the callback function self.cb

        """
        if self.pattern is not None:
            keys = self.r.keys(self.pattern)
            topics = [key.decode() for key in keys if key.decode().endswith(":stream")]
        else:
            topics = self.topics
        messages = []
        if self.newest_only:
            self.get_newest_message(messages)
        elif not self.from_start and not self.stream_keys:
            self.get_newest_message(messages, append=False)
        else:
            streams = {f"{topic}": self.get_id(topic) for topic in topics}
            read_msgs = self.r.xread(streams, count=1)
            if read_msgs:
                for msg in read_msgs:
                    topic = msg[0].decode()
                    messages.append((topic, msg[1][0][1]))
                    self.stream_keys[topic] = msg[1][-1][0]

        if messages:
            if MessageEndpoints.log() not in topics:
                # no need to update the update frequency just for logs
                self.last_received_msg = time.time()
            for topic, msg in messages:
                msg_obj = MessageObject(topic=topic, value=msg[b"data"])
                self.cb(msg_obj, **self.kwargs)
        else:
            sleep_time = int(bool(time.time() - self.last_received_msg > self.idle_time))
            if self.sleep_times[sleep_time]:
                time.sleep(self.sleep_times[sleep_time])


class RedisConsumerThreaded(RedisConsumerMixin, ConsumerConnectorThreaded):
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        host,
        port,
        topics=None,
        pattern=None,
        group_id=None,
        event=None,
        cb=None,
        redis_cls=None,
        name=None,
        **kwargs,
    ):
        self.host = host
        self.port = port

        bootstrap_server = "".join([host, ":", port])
        topics, pattern = self._init_topics_and_pattern(topics, pattern)
        super().__init__(
            bootstrap_server=bootstrap_server,
            topics=topics,
            pattern=pattern,
            group_id=group_id,
            event=event,
            cb=cb,
            name=name,
            **kwargs,
        )

        self._init_redis_cls(redis_cls)
        self.pubsub = self.r.pubsub()

        self.sleep_times = [0.005, 0.1]
        self.last_received_msg = 0
        self.idle_time = 30
        self.error_message_sent = False

    @catch_connection_error
    def poll_messages(self) -> None:
        """
        Poll messages from self.connector and call the callback function self.cb

        """
        messages = self.pubsub.get_message(ignore_subscribe_messages=True)
        if messages is not None:
            if f"{MessageEndpoints.log()}".encode() not in messages["channel"]:
                # no need to update the update frequency just for logs
                self.last_received_msg = time.time()
            msg = MessageObject(topic=messages["channel"], value=messages["data"])
            self.cb(msg, **self.kwargs)
        else:
            sleep_time = int(bool(time.time() - self.last_received_msg > self.idle_time))
            if self.sleep_times[sleep_time]:
                time.sleep(self.sleep_times[sleep_time])

    def shutdown(self):
        super().shutdown()
        self.pubsub.close()
