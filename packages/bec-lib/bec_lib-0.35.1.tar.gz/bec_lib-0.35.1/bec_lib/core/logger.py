from __future__ import annotations

import enum
import json
import sys
from typing import TYPE_CHECKING

from loguru import logger as loguru_logger

from . import BECMessage
from .endpoints import MessageEndpoints

if TYPE_CHECKING:
    from .connector import ConnectorBase


class LogLevel(int, enum.Enum):
    TRACE = 5
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class BECLogger:
    DEBUG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>[{level}]</level> | <level>{message}</level>"
    LOGLEVEL = LogLevel

    def __init__(self) -> None:
        if hasattr(self, "_configured"):
            return
        self.bootstrap_server = None
        self.connector = None
        self.service_name = None
        self.producer = None
        self.logger = loguru_logger
        self._log_level = LogLevel.INFO
        self.level = self._log_level
        self._configured = False

    def __new__(cls):
        if not hasattr(cls, "_logger"):
            cls._logger = super(BECLogger, cls).__new__(cls)
            cls._initialized = False
        return cls._logger

    def configure(
        self, bootstrap_server: list, connector_cls: ConnectorBase, service_name: str
    ) -> None:
        self.bootstrap_server = bootstrap_server
        self.connector = connector_cls(bootstrap_server)
        self.service_name = service_name
        self.producer = self.connector.producer()
        self._configured = True
        self._update_sinks()

    def _logger_callback(self, msg):
        if not self._configured:
            return
        msg = json.loads(msg)
        msg["service_name"] = self.service_name
        self.producer.send(
            topic=MessageEndpoints.log(),
            msg=BECMessage.LogMessage(log_type=msg["record"]["level"]["name"], content=msg).dumps(),
        )

    @property
    def format(self):
        if self.level > self.LOGLEVEL.DEBUG:
            return self.LOG_FORMAT

        return self.DEBUG_FORMAT

    def _update_sinks(self):
        self.logger.remove()
        self.add_redis_log(self._log_level)
        self.add_sys_stderr(self._log_level)
        self.add_file_log(self._log_level)

    def add_sys_stderr(self, level: LogLevel):
        self.logger.add(sys.stderr, level=level, format=self.format, enqueue=True)

    def add_file_log(self, level: LogLevel):
        if self.service_name:
            self.logger.add(
                f"{self.service_name}.log", level=level, format=self.format, enqueue=True
            )

    def add_redis_log(self, level: LogLevel):
        self.logger.add(self._logger_callback, serialize=True, level=level)

    @property
    def level(self):
        return self._log_level

    @level.setter
    def level(self, val: LogLevel):
        self._log_level = val
        self._update_sinks()


bec_logger = BECLogger()
