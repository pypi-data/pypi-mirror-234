import builtins
import os
import time
import uuid

import pytest
import yaml

import bec_lib.core
from bec_lib import BECClient
from bec_lib.core import BECMessage, MessageEndpoints, ServiceConfig, bec_logger
from bec_lib.core.connector import ConnectorBase
from bec_lib.core.redis_connector import Alarms
from bec_lib.devicemanager_client import DMClient
from bec_lib.scans import Scans

dir_path = os.path.dirname(bec_lib.core.__file__)

logger = bec_logger.logger

# pylint: disable=no-member
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access


def queue_is_empty(queue) -> bool:
    if not queue:
        return True
    if not queue["primary"].get("info"):
        return True
    return False


def get_queue(bec):
    return BECMessage.ScanQueueStatusMessage.loads(
        bec.queue.producer.get(MessageEndpoints.scan_queue_status())
    )


def wait_for_empty_queue(bec):
    while not get_queue(bec):
        time.sleep(1)
    while not queue_is_empty(get_queue(bec).content["queue"]):
        time.sleep(1)
        logger.info(bec.queue)
    while get_queue(bec).content["queue"]["primary"]["status"] != "RUNNING":
        time.sleep(1)
        logger.info(bec.queue)


class ScansMock(Scans):
    def _import_scans(self):
        pass

    def open_scan_def(self):
        pass

    def close_scan_def(self):
        pass

    def close_scan_group(self):
        pass

    def umv(self):
        pass


class ClientMock(BECClient):
    def _load_scans(self):
        self.scans = ScansMock(self)
        builtins.scans = self.scans

    def start(self):
        self._start_scan_queue()
        self._start_alarm_handler()

    def _start_metrics_emitter(self):
        pass

    def _start_update_service_info(self):
        pass


class DMClientMock(DMClient):
    def _get_device_info(self, device_name) -> BECMessage.DeviceInfoMessage:
        session_info = self.get_device(device_name)
        device_base_class = (
            "positioner"
            if session_info["acquisitionConfig"]["acquisitionGroup"] in ["motor"]
            else "signal"
        )
        if device_base_class == "positioner":
            signals = [
                "readback",
                "setpoint",
                "motor_is_moving",
                "velocity",
                "acceleration",
                "high_limit_travel",
                "low_limit_travel",
                "unused",
            ]
        elif device_base_class == "signal":
            signals = [
                "readback",
                "velocity",
                "acceleration",
                "high_limit_travel",
                "low_limit_travel",
                "unused",
            ]
        dev_info = {
            "device_name": device_name,
            "device_info": {"device_base_class": device_base_class, "signals": signals},
            "custom_user_acces": {},
        }
        return BECMessage.DeviceInfoMessage(device=device_name, info=dev_info, metadata={})

    def get_device(self, device_name):
        for dev in self._session["devices"]:
            if dev["name"] == device_name:
                return dev


@pytest.fixture()
def bec_client():
    client = ClientMock()
    client.initialize(
        ServiceConfig(redis={"host": "host", "port": 123}, scibec={"host": "host", "port": 123}),
        ConnectorMock,
    )
    device_manager = DMClientMock(client)
    if "test_session" not in builtins.__dict__:
        with open(f"{dir_path}/tests/test_config.yaml", "r", encoding="utf-8") as f:
            builtins.__dict__["test_session"] = create_session_from_config(yaml.safe_load(f))
    device_manager._session = builtins.__dict__["test_session"]
    device_manager.producer = device_manager.connector.producer()
    client.wait_for_service = lambda service_name: None
    device_manager._load_session()
    for name, dev in device_manager.devices.items():
        dev._info["hints"] = {"fields": [name]}
    client.device_manager = device_manager
    yield client
    ClientMock._client = None
    device_manager.devices.flush()


class PipelineMock:
    _pipe_buffer = []
    _producer = None

    def __init__(self, producer) -> None:
        self._producer = producer

    def execute(self):
        if not self._producer.store_data:
            self._pipe_buffer = []
            return []
        res = [
            getattr(self._producer, method)(*args, **kwargs)
            for method, args, kwargs in self._pipe_buffer
        ]
        self._pipe_buffer = []
        return res


class ConsumerMock:
    def __init__(self) -> None:
        self.signal_event = SignalMock()

    def start(self):
        pass

    def join(self):
        pass


class SignalMock:
    def __init__(self) -> None:
        self.is_set = False

    def set(self):
        self.is_set = True


class ProducerMock:
    def __init__(self, store_data=True) -> None:
        self.message_sent = []
        self._get_buffer = {}
        self.store_data = store_data

    def set(self, topic, msg, pipe=None, expire: int = None):
        if pipe:
            pipe._pipe_buffer.append(("set", (topic, msg), {"expire": expire}))
            return
        self.message_sent.append({"queue": topic, "msg": msg, "expire": expire})

    def send(self, topic, msg, pipe=None):
        if pipe:
            pipe._pipe_buffer.append(("send", (topic, msg), {}))
            return
        self.message_sent.append({"queue": topic, "msg": msg})

    def set_and_publish(self, topic, msg, pipe=None, expire: int = None):
        if pipe:
            pipe._pipe_buffer.append(("set_and_publish", (topic, msg), {"expire": expire}))
            return
        self.message_sent.append({"queue": topic, "msg": msg, "expire": expire})

    def lpush(self, topic, msg, pipe=None):
        if pipe:
            pipe._pipe_buffer.append(("lpush", (topic, msg), {}))
            return

    def rpush(self, topic, msg, pipe=None):
        if pipe:
            pipe._pipe_buffer.append(("rpush", (topic, msg), {}))
            return
        pass

    def lrange(self, topic, start, stop, pipe=None):
        if pipe:
            pipe._pipe_buffer.append(("lrange", (topic, start, stop), {}))
            return
        return []

    def get(self, topic, pipe=None):
        if pipe:
            pipe._pipe_buffer.append(("get", (topic,), {}))
            return
        val = self._get_buffer.get(topic)
        if isinstance(val, list):
            return val.pop(0)
        self._get_buffer.pop(topic, None)
        return val

    def keys(self, pattern: str) -> list:
        return []

    def pipeline(self):
        return PipelineMock(self)

    def delete(self, topic, pipe=None):
        if pipe:
            pipe._pipe_buffer.append(("delete", (topic,), {}))
            return

    def lset(self, topic: str, index: int, msgs: str, pipe=None) -> None:
        if pipe:
            pipe._pipe_buffer.append(("lrange", (topic, index, msgs), {}))
            return


class ConnectorMock(ConnectorBase):
    def __init__(self, bootstrap_server: list, store_data=True):
        super().__init__(bootstrap_server)
        self.store_data = store_data

    def consumer(self, *args, **kwargs) -> ConsumerMock:
        return ConsumerMock()

    def producer(self, *args, **kwargs):
        return ProducerMock(self.store_data)

    def raise_alarm(
        self, severity: Alarms, alarm_type: str, source: str, content: dict, metadata: dict
    ):
        pass

    def log_error(self, *args, **kwargs):
        pass


def create_session_from_config(config: dict) -> dict:
    device_configs = []
    session_id = str(uuid.uuid4())
    for name, conf in config.items():
        status = conf.pop("status")
        dev_conf = {
            "id": str(uuid.uuid4()),
            "accessGroups": "customer",
            "name": name,
            "sessionId": session_id,
            "enabled": status["enabled"],
            "enabled_set": status["enabled_set"],
        }
        dev_conf.update(conf)
        device_configs.append(dev_conf)
    session = {"accessGroups": "customer", "devices": device_configs}
    return session
