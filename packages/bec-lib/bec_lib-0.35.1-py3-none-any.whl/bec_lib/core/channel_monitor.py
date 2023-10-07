import argparse
import json
import threading

from bec_lib.core import BECMessage, RedisConnector, ServiceConfig

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "--config",
    default="",
    help="path to the config file",
)
parser.add_argument(
    "--channel",
    default="",
    help="channel name",
)
clargs = parser.parse_args()
config_path = clargs.config
topic = clargs.channel

config = ServiceConfig(config_path)


def channel_callback(msg, **kwargs):
    msg = BECMessage.MessageReader.loads(msg.value)
    out = {"msg_type": msg.msg_type, "content": msg.content, "metadata": msg.metadata}
    print(json.dumps(out, indent=4, default=lambda o: "<not serializable object>"))


connector = RedisConnector(config.redis)
consumer = connector.consumer(topics=topic, cb=channel_callback)
consumer.start()

event = threading.Event()
event.wait()
