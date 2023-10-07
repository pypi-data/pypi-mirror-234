from __future__ import annotations

import json
import time
import uuid
from typing import TYPE_CHECKING

import msgpack
import yaml

from .bec_errors import DeviceConfigError
from .BECMessage import DeviceConfigMessage, RequestResponseMessage
from .endpoints import MessageEndpoints
from .logger import bec_logger

if TYPE_CHECKING:
    from bec_lib.core import RedisConnector

logger = bec_logger.logger


class ConfigHelper:
    def __init__(self, connector: RedisConnector) -> None:
        self.connector = connector
        self.producer = connector.producer()

    def update_session_with_file(self, file_path: str, reload=True):
        """Update the current session with a yaml file from disk.

        Args:
            file_path (str): Full path to the yaml file.
            reload (bool, optional): Send a reload request to all services. Defaults to True.
        """
        config = self._load_config_from_file(file_path)
        self.send_config_request(action="set", config=config)

    def _load_config_from_file(self, file_path: str) -> dict:
        data = {}
        if not file_path.endswith(".yaml"):
            raise NotImplementedError

        with open(file_path, "r", encoding="utf-8") as stream:
            try:
                data = yaml.safe_load(stream)
                logger.trace(
                    f"Loaded new config from disk: {json.dumps(data, sort_keys=True, indent=4)}"
                )
            except yaml.YAMLError as err:
                logger.error(f"Error while loading config from disk: {repr(err)}")

        return data

    def save_current_session(self, file_path: str):
        """Save the current session as a yaml file to disk.

        Args:
            file_path (str): Full path to the yaml file.
        """
        msg_raw = self.producer.get(MessageEndpoints.device_config())
        config = msgpack.loads(msg_raw)
        out = {}
        for dev in config:
            dev.pop("id", None)
            dev.pop("createdAt", None)
            dev.pop("createdBy", None)
            dev.pop("sessionId", None)
            enabled = dev.pop("enabled", None)
            config = {"status": {"enabled": enabled}}

            enabled_set = dev.pop("enabled_set", None)
            if enabled_set is not None:
                config["status"]["enabled_set"] = enabled_set
            config.update(dev)
            out[dev["name"]] = config

        with open(file_path, "w") as file:
            file.write(yaml.dump(out))

        print(f"Config was written to {file_path}.")

    def send_config_request(self, action: str = "update", config=None) -> None:
        """
        send request to update config
        Returns:

        """
        if action in ["update", "add", "set"] and not config:
            raise DeviceConfigError(f"Config cannot be empty for an {action} request.")
        RID = str(uuid.uuid4())
        self.producer.send(
            MessageEndpoints.device_config_request(),
            DeviceConfigMessage(action=action, config=config, metadata={"RID": RID}).dumps(),
        )

        reply = self.wait_for_config_reply(RID)

        if not reply.content["accepted"]:
            raise DeviceConfigError(f"Failed to update the config: {reply.content['message']}.")

    def wait_for_config_reply(self, RID: str, timeout=10) -> RequestResponseMessage:
        """
        wait for config reply

        Args:
            RID (str): request id
            timeout (int, optional): timeout in seconds. Defaults to 10.

        Returns:
            RequestResponseMessage: reply message
        """
        start = 0
        while True:
            msg = self.producer.get(MessageEndpoints.device_config_request_response(RID))
            if msg is None:
                time.sleep(0.1)
                start += 0.1

                if start > timeout:
                    raise DeviceConfigError("Timeout reached whilst waiting for config reply.")
                continue
            return RequestResponseMessage.loads(msg)
