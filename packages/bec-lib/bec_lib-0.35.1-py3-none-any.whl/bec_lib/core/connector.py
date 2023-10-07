from __future__ import annotations

import _thread
import abc
import threading
import traceback

from .logger import bec_logger

logger = bec_logger.logger


class ConsumerConnectorError(Exception):
    pass


class MessageObject:
    def __init__(self, value, topic) -> None:
        self.topic = topic
        self._value = value

    @property
    def value(self):
        return self._value

    def __eq__(self, ref_val: MessageObject) -> bool:
        if not isinstance(ref_val, MessageObject):
            return False
        return self._value == ref_val.value and self.topic == ref_val.topic


class ConnectorBase(abc.ABC):
    """
    ConnectorBase implements producer and consumer clients for communicating with a broker.
    One ought to inherit from this base class and provide at least customized producer and consumer methods.

    """

    def __init__(self, bootstrap_server: list):
        self.bootstrap = bootstrap_server
        self._threads = []

    def producer(self, **kwargs) -> ProducerConnector:
        raise NotImplementedError

    def consumer(self, **kwargs) -> ConsumerConnectorThreaded:
        raise NotImplementedError

    def shutdown(self):
        for t in self._threads:
            t.signal_event.set()
            t.join()

    def raise_warning(self, msg):
        raise NotImplementedError

    def send_log(self, msg):
        raise NotImplementedError


class ProducerConnector(abc.ABC):
    def send(self, topic: str, msg) -> None:
        raise NotImplementedError


class ConsumerConnector(abc.ABC):
    def __init__(
        self,
        bootstrap_server,
        cb,
        topics=None,
        pattern=None,
        group_id=None,
        event=None,
        **kwargs,
    ):
        """
        ConsumerConnector class defines the communication with the broker for consuming messages.
        An implementation ought to inherit from this class and implement the initialize_connector and poll_messages methods.

        Args:
            bootstrap_server: list of bootstrap servers, e.g. ["localhost:9092", "localhost:9093"]
            topics: the topic(s) to which the connector should attach
            event: external event to trigger start and stop of the connector
            cb: callback function; will be triggered from within poll_messages
            kwargs: additional keyword arguments

        """
        self.bootstrap = bootstrap_server
        self.topics = topics
        self.pattern = pattern
        self.group_id = group_id
        self.connector = None
        self.cb = cb
        self.kwargs = kwargs

        if not self.topics and not self.pattern:
            raise ConsumerConnectorError("Either a topic or a patter must be specified.")

    def initialize_connector(self) -> None:
        """
        initialize the connector instance self.connector
        The connector will be initialized once the thread is started
        """
        raise NotImplementedError

    def poll_messages(self) -> None:
        """
        Poll messages from self.connector and call the callback function self.cb

        """
        messages = self.connector.poll(10.0)
        for _, values in messages.items():
            for msg in values:
                self.cb(msg, **self.kwargs)


class ConsumerConnectorThreaded(ConsumerConnector, threading.Thread):
    def __init__(
        self,
        bootstrap_server,
        cb,
        topics=None,
        pattern=None,
        group_id=None,
        event=None,
        name=None,
        **kwargs,
    ):
        """
        ConsumerConnectorThreaded class defines the threaded communication with the broker for consuming messages.
        An implementation ought to inherit from this class and implement the initialize_connector and poll_messages methods.
        Once started, the connector is expected to poll new messages until the signal_event is set.

        Args:
            bootstrap_server: list of bootstrap servers, e.g. ["localhost:9092", "localhost:9093"]
            topics: the topic(s) to which the connector should attach
            event: external event to trigger start and stop of the connector
            cb: callback function; will be triggered from within poll_messages
            kwargs: additional keyword arguments

        """
        super().__init__(
            bootstrap_server=bootstrap_server,
            topics=topics,
            pattern=pattern,
            group_id=group_id,
            event=event,
            cb=cb,
            **kwargs,
        )
        if name is not None:
            thread_kwargs = {"name": name, "daemon": True}
        else:
            thread_kwargs = {"daemon": True}
        super(ConsumerConnector, self).__init__(**thread_kwargs)
        self.signal_event = event if event is not None else threading.Event()

    def run(self):
        self.initialize_connector()

        while True:
            try:
                self.poll_messages()
            except Exception as e:
                logger.error(traceback.format_exc())
                _thread.interrupt_main()
                raise e
            finally:
                if self.signal_event.is_set():
                    self.shutdown()
                    break

    def shutdown(self):
        self.signal_event.set()

    # def stop(self) -> None:
    #     """
    #     Stop consumer
    #     Returns:

    #     """
    #     self.signal_event.set()
    #     self.connector.close()
    #     self.join()
