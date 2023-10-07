from __future__ import annotations

import functools
import threading
from collections import deque
from typing import TYPE_CHECKING, Deque, List, Optional

from bec_lib.core import BECMessage, MessageEndpoints, threadlocked
from rich.console import Console
from rich.table import Table

if TYPE_CHECKING:
    from request_items import RequestItem
    from scan_items import ScanItem
    from scan_manager import ScanManager


def update_queue(fcn):
    """Decorator to update the queue item"""

    @functools.wraps(fcn)
    def wrapper(self, *args, **kwargs):
        self._update_with_buffer()
        return fcn(self, *args, **kwargs)

    return wrapper


class QueueItem:
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        scan_manager: ScanManager,
        queueID: str,
        request_blocks: list,
        status: str,
        active_request_block: dict,
        scanID: List(str),
        **_kwargs,
    ) -> None:
        self.scan_manager = scan_manager
        self.queueID = queueID
        self.request_blocks = request_blocks
        self._status = status
        self.active_request_block = active_request_block
        self.scanIDs = scanID

    @property
    @update_queue
    def scans(self) -> List[ScanItem]:
        """get the scans items assigned to the current queue item"""
        return [self.scan_manager.scan_storage.find_scan_by_ID(scanID) for scanID in self.scanIDs]

    @property
    @update_queue
    def requestIDs(self):
        return [request_block["RID"] for request_block in self.request_blocks]

    @property
    @update_queue
    def requests(self) -> List[RequestItem]:
        """get the request items assigned to the current queue item"""
        return [
            self.scan_manager.request_storage.find_request_by_ID(requestID)
            for requestID in self.requestIDs
        ]

    @property
    @update_queue
    def status(self):
        return self._status

    def _update_with_buffer(self):
        current_queue = self.scan_manager.queue_storage.current_scan_queue
        queue_info = current_queue["primary"].get("info")
        for queue_item in queue_info:
            if queue_item["queueID"] == self.queueID:
                self.update_queue_item(queue_item)
                return
        history = self.scan_manager.queue_storage.queue_history()
        for queue_item in history:
            if queue_item.content["queueID"] == self.queueID:
                self.update_queue_item(queue_item.content["info"])
                return

    def update_queue_item(self, queue_item):
        """update the queue item"""
        self.request_blocks = queue_item.get("request_blocks")
        self._status = queue_item.get("status")
        self.active_request_block = queue_item.get("active_request_block")
        self.scanIDs = queue_item.get("scanID")

    @property
    def queue_position(self) -> Optional(int):
        """get the current queue position"""
        current_queue = self.scan_manager.queue_storage.current_scan_queue
        for queue_group in current_queue.values():
            if not isinstance(queue_group, dict):
                continue
            for queue_position, queue in enumerate(queue_group["info"]):
                if self.queueID == queue["queueID"]:
                    return queue_position
        return None


class QueueStorage:
    """stores queue items"""

    def __init__(self, scan_manager: ScanManager, maxlen=50) -> None:
        self.storage: Deque[QueueItem] = deque(maxlen=maxlen)
        self._lock = threading.RLock()
        self.scan_manager = scan_manager
        self._current_scan_queue = None

    def queue_history(self, history=5):
        """get the queue history of length 'history'"""
        if not history:
            raise ValueError("History length cannot be 0.")
        if history < 0:
            history *= -1

        return [
            BECMessage.ScanQueueHistoryMessage.loads(msg)
            for msg in self.scan_manager.producer.lrange(
                MessageEndpoints.scan_queue_history(),
                0,
                history,
            )
        ]

    @property
    def current_scan_queue(self) -> dict:
        """get the current scan queue from redis"""
        msg = BECMessage.ScanQueueStatusMessage.loads(
            self.scan_manager.producer.get(MessageEndpoints.scan_queue_status())
        )
        if msg:
            self._current_scan_queue = msg.content["queue"]
        return self._current_scan_queue

    @current_scan_queue.setter
    def current_scan_queue(self, val: dict):
        self._current_scan_queue = val

    def describe_queue(self):
        """create a rich.table description of the current scan queue"""
        queue_tables = []
        console = Console()
        for queue_name, scan_queue in self.current_scan_queue.items():
            table = Table(title=f"{queue_name} queue / {scan_queue.get('status')}")
            table.add_column("queueID", justify="center")
            table.add_column("scanID", justify="center")
            table.add_column("is_scan", justify="center")
            table.add_column("type", justify="center")
            table.add_column("scan_number", justify="center")
            table.add_column("IQ status", justify="center")

            for instruction_queue in scan_queue.get("info"):
                scan_msgs = [
                    msg.get("content") for msg in instruction_queue.get("request_blocks", [])
                ]
                table.add_row(
                    instruction_queue.get("queueID"),
                    ", ".join([str(s) for s in instruction_queue.get("scanID")]),
                    ", ".join([str(s) for s in instruction_queue.get("is_scan")]),
                    ", ".join([msg["scan_type"] for msg in scan_msgs]),
                    ", ".join([str(s) for s in instruction_queue.get("scan_number")]),
                    instruction_queue.get("status"),
                )
            with console.capture() as capture:
                console.print(table)
            queue_tables.append(capture.get())
        return queue_tables

    @threadlocked
    def update_with_status(self, queue_msg: BECMessage.ScanQueueStatusMessage) -> None:
        """update a queue item with a new ScanQueueStatusMessage / queue message"""
        self.current_scan_queue = queue_msg.content["queue"]
        queue_info = queue_msg.content["queue"]["primary"].get("info")
        for queue_item in queue_info:
            queue = self.find_queue_item_by_ID(queueID=queue_item["queueID"])
            if queue:
                queue.update_queue_item(queue_item)
                continue
            self.storage.append(QueueItem(scan_manager=self.scan_manager, **queue_item))

    @threadlocked
    def find_queue_item_by_ID(self, queueID: str) -> Optional(QueueItem):
        """find a queue item based on its queueID"""
        for queue_item in self.storage:
            if queue_item.queueID == queueID:
                return queue_item
        return None

    @threadlocked
    def find_queue_item_by_requestID(self, requestID: str) -> Optional(QueueItem):
        """find a queue item based on its requestID"""
        for queue_item in self.storage:
            if requestID in queue_item.requestIDs:
                return queue_item
        return None

    @threadlocked
    def find_queue_item_by_scanID(self, scanID: str) -> Optional(QueueItem):
        """find a queue item based on its scanID"""
        for queue_item in self.storage:
            if scanID in queue_item.scans:
                return queue_item
        return None
