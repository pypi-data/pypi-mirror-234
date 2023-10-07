import argparse

import msgpack
import yaml
from bec_lib.core import MessageEndpoints, RedisConnector

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "--config",
    default="./init_scibec/demo_config.yaml",
    help="path to the config file",
)
parser.add_argument(
    "--redis",
    default="localhost:6379",
    help="redis host and port",
)

clargs = parser.parse_args()
connector = RedisConnector(clargs.redis)
producer = connector.producer()

with open(clargs.config, "r", encoding="utf-8") as stream:
    data = yaml.safe_load(stream)
for name, device in data.items():
    device["enabled"] = device["status"]["enabled"]
    if device["status"].get("enabled_set"):
        device["enabled_set"] = device["status"].get("enabled_set")
    device.pop("status")
    device["name"] = name
config_data = list(data.values())
producer.set(MessageEndpoints.device_config(), msgpack.dumps(config_data))
