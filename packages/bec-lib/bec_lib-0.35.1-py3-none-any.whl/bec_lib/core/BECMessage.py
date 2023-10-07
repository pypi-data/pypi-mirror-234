from __future__ import annotations

import base64
import enum
import inspect
import json
import sys
import time
from abc import abstractmethod
from copy import deepcopy
from typing import Any, List, Optional, Union

import msgpack
import numpy as np

from .logger import bec_logger
from .numpy_encoder import numpy_decode, numpy_encode

logger = bec_logger.logger

BECCOMPRESSION = "msgpack"
DEFAULT_VERSION = 1.2


class BECMessageCompression:
    """Base class for message compression"""

    @abstractmethod
    def loads(self, msg, **kwargs) -> dict:
        """load and decompress a message"""

    @abstractmethod
    def dumps(self, msg, **kwargs) -> str:
        """compress a message"""


class MsgpackCompression(BECMessageCompression):
    """Message compression using msgpack and base64 encoding"""

    def loads(self, msg, encode=True, **kwargs) -> dict:
        if not encode:
            return msgpack.loads(msg, raw=False, object_hook=numpy_decode)
        return msgpack.loads(base64.b64decode(msg.encode()), object_hook=numpy_decode)

    def dumps(self, msg, encode=True, **kwargs) -> str:
        if not encode:
            return msgpack.dumps(msg, default=numpy_encode)
        return base64.b64encode(msgpack.dumps(msg, default=numpy_encode)).decode()


class JsonCompression(BECMessageCompression):
    """Message compression using json"""

    def loads(self, msg, **kwargs):
        return json.loads(msg)

    def dumps(self, msg, **kwargs):
        return json.dumps(msg)


class BECStatus(enum.Enum):
    """BEC status enum"""

    RUNNING = 2
    BUSY = 1
    IDLE = 0
    ERROR = -1


class BECMessage:
    """Base class for all BEC messages"""

    msg_type: str
    content: dict
    metadata: dict

    def __init__(
        self,
        *,
        msg_type: str,
        content: dict,
        metadata: dict = None,
        version: float = DEFAULT_VERSION,
    ) -> None:
        self.msg_type = msg_type
        self.content = content
        self.metadata = metadata if metadata is not None else {}
        self.version = version
        self.compression = BECCOMPRESSION
        self.compression_handler = self._get_compression_handler()

    @staticmethod
    def _get_compression_handler(compression: str = BECCOMPRESSION) -> BECMessageCompression:
        if compression == "msgpack":
            return MsgpackCompression()
        if compression == "json":
            return JsonCompression()
        raise RuntimeError(f"Unsupported compression type {compression}.")

    @classmethod
    def loads(cls, msg) -> Optional(BECMessage):
        """load BECMessage from bytes or dict input"""
        try:
            if isinstance(msg, bytes) and msg.startswith(b"MSGVERSION_"):
                version = float(msg[11:14])
            else:
                msg = json.loads(msg)
                version = msg["version"]
        except Exception:
            version = 1.0

        if version == 1.0:
            if isinstance(msg, bytes):
                msg = msgpack.loads(msg, raw=False, object_hook=numpy_decode)
                if msg["msg_type"] == "bundle_message":
                    return [
                        cls._validated_return(
                            msgpack.loads(sub_message, raw=False, object_hook=numpy_decode)
                        )
                        for sub_message in msg["content"]["messages"]
                    ]
                return cls._validated_return(msg)
            if isinstance(msg, dict):
                return cls(metadata=msg.get("metadata"), **msg.get("content", {}))
            return None
        if version == 1.1:
            msg_compression = msg.get("compression")
            compression_handler = cls._get_compression_handler(msg_compression)
            msg["body"] = compression_handler.loads(msg.get("body"))
            if msg["msg_type"] == "bundle_message":
                msgs = msg["body"]["content"]["messages"]
                ret = []
                for sub_message in msgs:
                    msg_cls = cls.get_message_class(sub_message)
                    ret.append(msg_cls.loads(sub_message))
                return ret
            return cls._validated_return(msg)
        if version == 1.2:
            declaration, msg_header_body = msg.split(b"_EOH_", maxsplit=1)
            _, version, header_length, _ = declaration.split(b"_")
            header = msg_header_body[: int(header_length)]
            body = msg_header_body[int(header_length) :]
            header = json.loads(header.decode())
            msg_compression = header.get("compression")
            compression_handler = cls._get_compression_handler(msg_compression)
            msg_out = {**header, "body": compression_handler.loads(body, encode=False)}
            if header["msg_type"] == "bundle_message":
                msgs = msg_out["body"]["content"]["messages"]
                ret = []
                for sub_message in msgs:
                    msg_cls = cls.get_message_class(sub_message)
                    ret.append(msg_cls.loads(sub_message))
                return ret
            return cls._validated_return(msg_out)
        raise RuntimeError(f"Unsupported BECMessage version {version}.")

    def dumps(self):
        """dump BECMessage with msgpack"""
        if self.version == 1.0:
            msg = {
                "msg_type": self.msg_type,
                "content": self.content,
                "metadata": self.metadata,
                "version": self.version,
                "compression": self.compression,
            }
            return self.compression_handler.dumps(msg, encode=False)
        if self.version == 1.1:
            msg = {
                "content": self.content,
                "metadata": self.metadata,
            }
            msg_header = {
                "msg_type": self.msg_type,
                "version": self.version,
                "compression": self.compression,
            }
            msg_body = self.compression_handler.dumps(msg)
            return json.dumps(
                {
                    **msg_header,
                    "body": msg_body,
                }
            )
        if self.version == 1.2:
            msg = {
                "content": self.content,
                "metadata": self.metadata,
            }
            msg_header = json.dumps(
                {
                    "msg_type": self.msg_type,
                    "version": self.version,
                    "compression": self.compression,
                }
            ).encode()
            msg_body = self.compression_handler.dumps(msg, encode=False)
            if not isinstance(msg_body, bytes):
                msg_body = msg_body.encode()
            header = f"MSGVERSION_{self.version}_{len(msg_header)}_{len(msg_body)}_EOH_".encode()
            return header + msg_header + msg_body

    @classmethod
    def _validated_return(cls, msg):
        version = msg.get("version")
        if version == 1.0:
            msg_body = msg
        else:
            msg_body = msg.get("body")
        if cls.msg_type != msg.get("msg_type"):
            logger.warning(f"Invalid message type: {msg.get('msg_type')}")
            return None
        msg_conv = cls(**msg_body.get("content"), metadata=msg_body.get("metadata"))
        if msg_conv._is_valid():
            return msg_conv
        logger.warning(f"Invalid message: {msg_conv}")
        return None

    def _is_valid(self) -> bool:
        return True

    def __eq__(self, other):
        if not isinstance(other, BECMessage):
            # don't attempt to compare against unrelated types
            return False

        try:
            np.testing.assert_equal(self.content, other.content)
        except AssertionError:
            return False

        return self.msg_type == other.msg_type and self.metadata == other.metadata

    def __repr__(self):
        return f"BECMessage.{self.__class__.__name__}(**{self.content}, metadata={self.metadata})"

    def __str__(self):
        return f"BECMessage.{self.__class__.__name__}(**{self.content}, metadata={self.metadata})"

    @staticmethod
    def get_message_class(msg: str) -> BECMessage:
        """get the BECMessage class from the message's msg_type"""
        if isinstance(msg, bytes) and msg.startswith(b"MSGVERSION_"):
            declaration, msg_header_body = msg.split(b"_EOH_", maxsplit=1)
            _, version, header_length, _ = declaration.split(b"_")
            header = msg_header_body[: int(header_length)]
            msg_json = json.loads(header.decode())
        else:
            msg_json = json.loads(msg)
        module_members = inspect.getmembers(sys.modules[__name__], inspect.isclass)
        bec_classes = {mem.msg_type: mem for _, mem in module_members if hasattr(mem, "msg_type")}
        msg_class = bec_classes[msg_json["msg_type"]]
        return msg_class


class BundleMessage(BECMessage):
    """Bundle of BECMessages"""

    msg_type = "bundle_message"

    def __init__(
        self,
        *,
        messages: list = None,
        metadata: dict = None,
        version: float = DEFAULT_VERSION,
        **_kwargs,
    ) -> None:
        content = {}
        super().__init__(
            msg_type=self.msg_type, content=content, metadata=metadata, version=version
        )
        self.content["messages"] = [] if not messages else messages

    def append(self, msg: BECMessage):
        """append a new BECMessage to the bundle"""
        if isinstance(msg, bytes) or isinstance(msg, str):
            self.content["messages"].append(msg)
        elif isinstance(msg, BECMessage):
            self.content["messages"].append(msg.dumps())
        else:
            raise AttributeError(f"Cannot append message of type {msg.__class__.__name__}")

    def __len__(self):
        return len(self.content["messages"])


class MessageReader(BECMessage):
    """MessageReader class for loading arbitrary BECMessages

    Examples:
        >>> msg = MessageReader.loads(input_msg)

    """

    def __init__(
        self,
        *,
        msg_type: str,
        content: dict,
        metadata: dict = None,
        version: float = DEFAULT_VERSION,
        **_kwargs,
    ) -> None:
        super().__init__(msg_type=msg_type, content=content, metadata=metadata, version=version)

    @classmethod
    def _validated_return(cls, msg):
        msg_conv = cls(**msg)
        return msg_conv

    @classmethod
    def loads(cls, msg):
        msg_class = cls.get_message_class(msg)
        return msg_class.loads(msg)

    @classmethod
    def dumps(cls, msg):
        raise NotImplementedError("MessageReader can only be used to load data.")


class ScanQueueMessage(BECMessage):
    """Message type for sending scan requests to the scan queue"""

    msg_type = "scan"

    def __init__(
        self,
        *,
        scan_type: str,
        parameter: dict,
        queue="primary",
        metadata: dict = None,
        version: float = DEFAULT_VERSION,
    ) -> None:
        """
        Sent by the API server / user to the scan_queue topic. It will be consumed by the scan server.
        Args:
            scan_type: one of the registered scan types; either scan stubs (set, read, ...) or scans (dscan, ct, ...)
            parameter: required parameters for the given scan_stype
            queue: either "primary" or "interception"
            metadata: additional metadata to describe the scan
        Examples:
            >>> ScanQueueMessage(scan_type="dscan", parameter={"motor1": "samx", "from_m1:": -5, "to_m1": 5, "steps_m1": 10, "motor2": "samy", "from_m2": -5, "to_m2": 5, "steps_m2": 10, "exp_time": 0.1})
        """

        self.content = {"scan_type": scan_type, "parameter": parameter, "queue": queue}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class ScanQueueHistoryMessage(BECMessage):
    """Sent after removal from the active queue. Contains information about the scan."""

    msg_type = "queue_history"

    def __init__(
        self,
        *,
        status: str,
        queueID: str,
        info=dict,
        queue="primary",
        metadata: dict = None,
        version: float = DEFAULT_VERSION,
    ) -> None:
        self.content = {"status": status, "queueID": queueID, "info": info, "queue": queue}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class ScanStatusMessage(BECMessage):
    """Message type for sending scan status updates"""

    msg_type = "scan_status"

    def __init__(
        self,
        *,
        scanID: str,
        status: dict,
        info: dict,
        timestamp: float = None,
        metadata: dict = None,
        version: float = DEFAULT_VERSION,
    ) -> None:
        """
        Args:
            scanID(str): unique scan ID
            status(dict): dictionary containing the current scan status
            info(dict): dictionary containing additional information about the scan
            timestamp(float): timestamp of the scan status update. If None, the current time is used.
            metadata(dict): additional metadata to describe and identify the scan.
            version(float): BECMessage version

        Examples:
            >>> ScanStatusMessage(scanID="1234", status={"scan_number": 1, "scan_motors": ["samx", "samy"], "scan_type": "dscan", "scan_status": "RUNNING"}, info={"positions": {"samx": 0.5, "samy": 0.5}})
        """
        tms = timestamp if timestamp is not None else time.time()
        self.content = {"scanID": scanID, "status": status, "info": info, "timestamp": tms}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )

    def __str__(self):
        content = deepcopy(self.content)
        if content["info"].get("positions"):
            content["info"]["positions"] = "..."
        return f"{self.__class__.__name__}({content, self.metadata}))"


class ScanQueueModificationMessage(BECMessage):
    """Message type for sending scan queue modifications"""

    msg_type = "scan_queue_modification"
    ACTIONS = ["pause", "deferred_pause", "continue", "abort", "clear", "restart", "halt"]

    def __init__(
        self,
        *,
        scanID: str,
        action: str,
        parameter: dict,
        metadata: dict = None,
        version: float = DEFAULT_VERSION,
    ) -> None:
        self.content = {"scanID": scanID, "action": action, "parameter": parameter}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )

    def _is_valid(self) -> bool:
        if not self.content.get("action") in self.ACTIONS:
            return False
        return True


class ScanQueueStatusMessage(BECMessage):
    """Message type for sending scan queue status updates"""

    msg_type = "scan_queue_status"

    def __init__(
        self, *, queue: dict, metadata: dict = None, version: float = DEFAULT_VERSION
    ) -> None:
        self.content = {"queue": queue}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )

    def _is_valid(self) -> bool:
        if (
            not isinstance(self.content["queue"], dict)
            or not "primary" in self.content["queue"]
            or not isinstance(self.content["queue"]["primary"], dict)
        ):
            return False
        return True


class RequestResponseMessage(BECMessage):
    """Message type for sending back decisions on the acceptance of requests"""

    msg_type = "request_response"

    def __init__(
        self,
        *,
        accepted: bool,
        message: str,
        metadata: dict = None,
        version: float = DEFAULT_VERSION,
    ) -> None:
        """
        Message type for sending back decisions on the acceptance of requests.
        Args:
            accepted: True if the request was accepted
            message: String describing the decision, e.g. "Invalid request"
            metadata: additional metadata to describe and identify the request / response
        """

        self.content = {"accepted": accepted, "message": message}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class DeviceInstructionMessage(BECMessage):
    """Message type for sending device instructions to the device server"""

    msg_type = "device_instruction"

    def __init__(
        self,
        *,
        device: str,
        action: str,
        parameter: dict,
        metadata: dict = None,
        version: float = DEFAULT_VERSION,
    ) -> None:
        """

        Args:
            device:
            action:
            parameter:
        """
        self.content = {"device": device, "action": action, "parameter": parameter}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class DeviceMessage(BECMessage):
    """Message type for sending device readings from the device server"""

    msg_type = "device_message"

    def __init__(
        self, *, signals: dict, metadata: dict = None, version: float = DEFAULT_VERSION
    ) -> None:
        """
        Device message type for sending device readings from the device server.

        Args:
            signals: dictionary of device signals
            metadata: metadata to describe the conditions of the device reading
        Examples:
            >>> BECMessage.DeviceMessage(signals={'samx': {'value': 14.999033949016491, 'timestamp': 1686385306.0265112}, 'samx_setpoint': {'value': 15.0, 'timestamp': 1686385306.016806}, 'samx_motor_is_moving': {'value': 0, 'timestamp': 1686385306.026888}}}, metadata={'stream': 'primary', 'DIID': 353, 'RID': 'd3471acc-309d-43b7-8ff8-f986c3fdecf1', 'pointID': 49, 'scanID': '8e234698-358e-402d-a272-73e168a72f66', 'queueID': '7a232746-6c90-44f5-81f5-74ab0ea22d4a'})
        """
        self.content = {"signals": signals}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )

    def _is_valid(self) -> bool:
        if not isinstance(self.content["signals"], dict):
            return False
        return True


class DeviceRPCMessage(BECMessage):
    """Message type for sending device RPC return values from the device server"""

    msg_type = "device_rpc_message"

    def __init__(
        self,
        *,
        device: str,
        return_val: Any,
        out: str,
        success: bool = True,
        metadata: dict = None,
        version: float = DEFAULT_VERSION,
    ) -> None:
        """

        Args:
            signals:
            metadata:
        """
        self.content = {"device": device, "return_val": return_val, "out": out, "success": success}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )

    def _is_valid(self) -> bool:
        if not isinstance(self.content["device"], str):
            return False
        return True


class DeviceStatusMessage(BECMessage):
    """Message type for sending device status updates from the device server"""

    msg_type = "device_status_message"

    def __init__(
        self, *, device: str, status: int, metadata: dict = None, version: float = DEFAULT_VERSION
    ) -> None:
        """

        Args:
            signals:
            metadata:
        """
        self.content = {"device": device, "status": status}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class DeviceReqStatusMessage(BECMessage):
    """Message type for sending device request status updates from the device server"""

    msg_type = "device_req_status_message"

    def __init__(
        self, *, device: str, success: bool, metadata: dict = None, version: float = DEFAULT_VERSION
    ) -> None:
        """

        Args:
            signals:
            metadata:
        """
        self.content = {"device": device, "success": success}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class DeviceInfoMessage(BECMessage):
    """Message type for sending device info updates from the device server"""

    msg_type = "device_info_message"

    def __init__(
        self, *, device: str, info: dict, metadata: dict = None, version: float = DEFAULT_VERSION
    ) -> None:
        """

        Args:
            device:
            info:
            metadata:
        """
        self.content = {"device": device, "info": info}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class ScanMessage(BECMessage):
    """Message type for sending scan segment data from the scan bundler"""

    msg_type = "scan_message"

    def __init__(
        self,
        *,
        point_id: int,
        scanID: int,
        data: dict,
        metadata: dict = None,
        version: float = DEFAULT_VERSION,
    ) -> None:
        """

        Args:
            point_id:
            scanID:
            data:
        """
        self.content = {"point_id": point_id, "scanID": scanID, "data": data}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class ScanBaselineMessage(BECMessage):
    """Message type for sending scan baseline data from the scan bundler"""

    msg_type = "scan_baseline_message"

    def __init__(
        self, *, scanID: int, data: dict, metadata: dict = None, version: float = DEFAULT_VERSION
    ) -> None:
        """

        Args:
            scanID:
            data:
        """
        self.content = {"scanID": scanID, "data": data}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class DeviceConfigMessage(BECMessage):
    """Message type for sending device config updates"""

    msg_type = "device_config_message"

    def __init__(
        self, *, action: str, config: dict, metadata: dict = None, version: float = DEFAULT_VERSION
    ) -> None:
        """

        Args:
            action: add, update or reload
            config: device config (add, update) or None (reload)
        """
        self.content = {"action": action, "config": config}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class LogMessage(BECMessage):
    """Log message"""

    msg_type = "log_message"

    def __init__(
        self,
        *,
        log_type: str,
        content: Union[dict, str],
        metadata: dict = None,
        version: float = DEFAULT_VERSION,
    ) -> None:
        """

        Args:
            type: log, warning or error
            content: log's content
        """
        self.content = {"log_type": log_type, "content": content}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class AlarmMessage(BECMessage):
    """Alarm message"""

    msg_type = "alarm_message"

    def __init__(
        self,
        *,
        severity: int,
        alarm_type=str,
        source: str,
        content: dict,
        metadata: dict = None,
        version: float = DEFAULT_VERSION,
    ) -> None:
        """Alarm message
        Severity 1: Minor alarm, no user interaction needed. The system can continue.
        Severity 2: Major alarm, user interaction needed. If the alarm was raised during the execution of a request, the request will be paused until the alarm is resolved.
        Severity 3: Major alarm, user interaction needed. The system cannot recover by itself.

        Args:
            severity (int): severity level (1-3)
            source (str): source of the problem (where did it occur?)
            content (dict): problem description (what happened?)
            metadata (dict, optional)
        """
        self.content = {
            "severity": severity,
            "alarm_type": alarm_type,
            "source": source,
            "content": content,
        }
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class StatusMessage(BECMessage):
    """Status message"""

    msg_type = "status_message"

    def __init__(
        self,
        *,
        name: str,
        status: BECStatus,
        info: dict,
        metadata: dict = None,
        version: float = DEFAULT_VERSION,
    ) -> None:
        """

        Args:
            status: error, off, idle or running
            metadata: status metadata
        """
        if not isinstance(status, BECMessage):
            status = BECStatus(status)
        self.content = {"name": name, "status": status.value, "info": info}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class FileMessage(BECMessage):
    """File message to inform about the status of a file writing operation"""

    msg_type = "file_message"

    def __init__(
        self,
        *,
        file_path: str,
        done: bool = True,
        successful: bool = True,
        metadata: dict = None,
        version: float = DEFAULT_VERSION,
    ) -> None:
        """
        Args:
            file_path (str): path to the file
            done (bool, optional): True if the file writing operation is done. Defaults to True.
            successful (bool, optional): True if the file writing operation was successful. Defaults to True.
            metadata (dict, optional): status metadata. Defaults to None.
            version (float, optional): BECMessage version. Defaults to DEFAULT_VERSION.
        """

        self.content = {"file_path": file_path, "done": done, "successful": successful}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class VariableMessage(BECMessage):
    """Message to inform about a global variable"""

    msg_type = "var_message"

    def __init__(
        self, *, value: str, metadata: dict = None, version: float = DEFAULT_VERSION
    ) -> None:
        """
        Args:
            value: value of the global var
            metadata: status metadata
        """

        self.content = {"value": value}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class ObserverMessage(BECMessage):
    """Message for observer updates"""

    msg_type = "observer_message"

    def __init__(
        self, *, observer: List[dict], metadata: dict = None, version: float = DEFAULT_VERSION
    ) -> None:
        """

        Args:
            observer: list of observer descriptions
            metadata: status metadata
        """

        self.content = {"observer": observer}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class ServiceMetricMessage(BECMessage):
    """Message for service metrics"""

    msg_type = "service_metric_message"

    def __init__(
        self, *, name: str, metrics: dict, metadata: dict = None, version: float = DEFAULT_VERSION
    ) -> None:
        """

        Args:
            observer: list of observer descriptions
            metadata: status metadata
        """

        self.content = {"name": name, "metrics": metrics}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class ProcessedDataMessage(BECMessage):
    """Message for processed data"""

    msg_type = "processed_data_message"

    def __init__(
        self, *, data: str, metadata: dict = None, version: float = DEFAULT_VERSION
    ) -> None:
        """
        Message for processed data
        Args:
            data (str): processed data
            metadata (dict, optional): metadata. Defaults to None.
        """

        self.content = {"data": data}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class DAPConfigMessage(BECMessage):
    """Message for DAP configuration"""

    msg_type = "dap_config_message"

    def __init__(
        self, *, config: dict, metadata: dict = None, version: float = DEFAULT_VERSION
    ) -> None:
        """
        Message for DAP configuration
        Args:
            config (dict): DAP configuration
            metadata (dict, optional): metadata. Defaults to None.
        """

        self.content = {"config": config}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class AvailableResourceMessage(BECMessage):
    """Message for available resources such as scans, data processing plugins etc"""

    msg_type = "available_resource_message"

    def __init__(
        self, *, resource: dict, metadata: dict = None, version: float = DEFAULT_VERSION
    ) -> None:
        """
        Message for available resources such as scans, data processing plugins etc
        Args:
            ressource (dict): resource description
            metadata (dict, optional): metadata. Defaults to None.
        """

        self.content = {"resource": resource}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )


class ProgressMessage(BECMessage):
    """Message for communicating the progress of a long running task"""

    msg_type = "progress_message"

    def __init__(
        self,
        *,
        value: float,
        max_value: float,
        done: bool,
        metadata: dict = None,
        version: float = DEFAULT_VERSION,
    ) -> None:
        """
        Message for communicating the progress of a long running task

        Args:
            value (float): current progress value
            max_value (float): maximum progress value
            done (bool): True if the task is done
            metadata (dict, optional): metadata. Defaults to None.
        """

        self.content = {"value": value, "max_value": max_value, "done": done}
        super().__init__(
            msg_type=self.msg_type, content=self.content, metadata=metadata, version=version
        )
