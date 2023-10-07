import threading
from collections import deque
from typing import List

from bec_lib.core import (
    Alarms,
    BECMessage,
    MessageEndpoints,
    RedisConnector,
    bec_logger,
    threadlocked,
)

logger = bec_logger.logger


class AlarmException(Exception):
    pass


class AlarmBase(Exception):
    def __init__(
        self, alarm: BECMessage.AlarmMessage, alarm_type: str, severity: Alarms, handled=False
    ) -> None:
        self.alarm = alarm
        self.severity = severity
        self.handled = handled
        self.alarm_type = alarm_type
        super().__init__(self.alarm.content)

    def __str__(self) -> str:
        self.handled = True
        return f"An alarm has occured. Severity: {self.severity.name}. Source: {self.alarm.content['source']}.\n{self.alarm_type}.\n\t {self.alarm.content['content']}"

    def __repr__(self) -> str:
        return f"Severity: {self.severity.name} \nAlarm type: {self.alarm_type} \nSource: {self.alarm.content['source']} \n{self.alarm.content['content']}"


class AlarmHandler:
    def __init__(self, connector: RedisConnector) -> None:
        self.connector = connector
        self.alarm_consumer = None
        self.alarms_stack = deque(maxlen=100)
        self._raised_alarms = deque(maxlen=100)
        self._lock = threading.RLock()

    def start(self):
        """start the alarm handler and its subscriptions"""
        self.alarm_consumer = self.connector.consumer(
            topics=MessageEndpoints.alarm(), cb=self._alarm_consumer_callback, parent=self
        )
        self.alarm_consumer.start()

    @staticmethod
    def _alarm_consumer_callback(msg, *, parent, **_kwargs):
        msg = BECMessage.AlarmMessage.loads(msg.value)
        parent.add_alarm(msg)

    @threadlocked
    def add_alarm(self, msg: BECMessage.AlarmMessage):
        """Add a new alarm message to the stack.

        Args:
            msg (BECMessage.AlarmMessage): Alarm message that should be added
        """
        severity = Alarms(msg.content["severity"])
        alarm = AlarmBase(
            alarm=msg, alarm_type=msg.content["alarm_type"], severity=severity, handled=False
        )
        if severity > Alarms.MINOR:
            self.alarms_stack.appendleft(alarm)
            logger.debug(alarm)
        else:
            logger.warning(alarm)

    @threadlocked
    def get_unhandled_alarms(self, severity=Alarms.WARNING) -> List:
        """Get all unhandled alarms equal or above a minimum severity.

        Args:
            severity (Alarms, optional): Minimum severity. Defaults to Alarms.WARNING.

        Returns:
            list: List of unhandled alarms

        """
        return [
            alarm for alarm in self.alarms_stack if not alarm.handled and alarm.severity >= severity
        ]

    @threadlocked
    def get_alarm(self, severity=Alarms.WARNING):
        """Get the next alarm

        Args:
            severity (Alarm, optional): Minimum severity. Defaults to Alarms.WARNING.

        Yields:
            AlarmBase: Alarm
        """
        alarms = self.get_unhandled_alarms(severity=severity)
        for alarm in alarms:
            self.alarms_stack.remove(alarm)
            yield alarm

    def raise_alarms(self, severity=Alarms.MAJOR):
        """Raise unhandled alarms with specified severity.

        Args:
            severity (Alarm, optional): Minimum severity. Defaults to Alarms.MAJOR.

        Raises:
            alarms: Alarm exception.
        """
        alarms = self.get_unhandled_alarms(severity=severity)
        if len(alarms) > 0:
            self._raised_alarms.append(alarms[0])
            raise alarms[0]

    @threadlocked
    def clear(self):
        """clear all alarms from stack"""
        self.alarms_stack.clear()

    def shutdown(self):
        """shutdown the alarm handler"""
        self.alarm_consumer.shutdown()
