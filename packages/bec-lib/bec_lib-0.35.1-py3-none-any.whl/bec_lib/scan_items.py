from __future__ import annotations

import builtins
import datetime
import sys
import threading
import time
from collections import defaultdict, deque
from typing import TYPE_CHECKING, Optional

from bec_lib.core import BECMessage, bec_logger, threadlocked

if TYPE_CHECKING:
    from bec_lib.scan_manager import ScanManager

logger = bec_logger.logger

try:
    import pandas as pd
except ImportError:
    logger.info("Unable to import `pandas` optional dependency")


class ScanItem:
    status: dict

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        scan_manager: ScanManager,
        queueID: str,
        scan_number: list,
        scanID: list,
        status: str,
        **_kwargs,
    ) -> None:
        self.scan_manager = scan_manager
        self._queueID = queueID
        self.scan_number = scan_number
        self.scanID = scanID
        self.status = status
        self.data = {}
        self.open_scan_defs = set()
        self.open_queue_group = None
        self.num_points = None
        self.start_time = None
        self.end_time = None
        self.scan_report_instructions = []
        self.callbacks = []
        self.bec = builtins.__dict__.get("bec")

    @property
    def queue(self):
        """get the queue item for the current scan item"""
        return self.scan_manager.queue_storage.find_queue_item_by_ID(self._queueID)

    def emit_data(self, scan_msg: BECMessage.ScanMessage) -> None:
        self.bec.callbacks.run("scan_segment", scan_msg.content, scan_msg.metadata)
        self._run_request_callbacks("scan_segment", scan_msg.content, scan_msg.metadata)

    def emit_status(self, scan_status: BECMessage.ScanStatusMessage) -> None:
        self.bec.callbacks.run("status", scan_status.content, scan_status.metadata)
        self._run_request_callbacks("status", scan_status.content, scan_status.metadata)

    def _run_request_callbacks(self, event_type: str, data: dict, metadata: dict):
        for rid in self.queue.requestIDs:
            req = self.scan_manager.request_storage.find_request_by_ID(rid)
            req.callbacks.run(event_type, data, metadata)

    def poll_callbacks(self):
        for rid in self.queue.requestIDs:
            req = self.scan_manager.request_storage.find_request_by_ID(rid)
            req.callbacks.poll()

    def to_pandas(self) -> pd.DataFrame:
        """convert to pandas dataframe"""
        if "pandas" not in sys.modules:
            raise ImportError("Install `pandas` to use to_pandas() method")

        tmp = defaultdict(list)
        for scan_msg in self.data.values():
            scan_msg_data = scan_msg.content["data"]
            for dev, dev_data in scan_msg_data.items():
                for signal, signal_data in dev_data.items():
                    for key, value in signal_data.items():
                        tmp[(dev, signal, key)].append(value)

        return pd.DataFrame(tmp)

    def __eq__(self, other):
        return self.scanID == other.scanID

    def describe(self) -> str:
        """describe the scan item"""
        start_time = (
            f"\tStart time: {datetime.datetime.fromtimestamp(self.start_time).strftime('%c')}\n"
            if self.start_time
            else ""
        )
        end_time = (
            f"\tEnd time: {datetime.datetime.fromtimestamp(self.end_time).strftime('%c')}\n"
            if self.end_time
            else ""
        )
        elapsed_time = (
            f"\tElapsed time: {(self.end_time-self.start_time):.1f} s\n"
            if self.end_time and self.start_time
            else ""
        )
        scanID = f"\tScan ID: {self.scanID}\n" if self.scanID else ""
        scan_number = f"\tScan number: {self.scan_number}\n" if self.scan_number else ""
        num_points = f"\tNumber of points: {self.num_points}\n" if self.num_points else ""
        details = start_time + end_time + elapsed_time + scanID + scan_number + num_points
        return details

    def __repr__(self) -> str:
        return f"ScanItem:\n {self.describe()}"


class ScanStorage:
    """stores scan items"""

    def __init__(self, scan_manager: ScanManager, maxlen=50, init_scan_number=0) -> None:
        self.scan_manager = scan_manager
        self.storage = deque(maxlen=maxlen)
        self.last_scan_number = init_scan_number
        self._lock = threading.RLock()

    @property
    def current_scan_info(self) -> dict:
        """get the current scan info from the scan queue"""
        scan_queue = self.scan_manager.queue_storage.current_scan_queue
        if not scan_queue or not scan_queue["primary"].get("info"):
            return None
        return scan_queue["primary"].get("info")[0]

    @property
    def current_scan(self) -> Optional(ScanItem):
        """get the current scan item"""
        if not self.current_scanID:
            return None
        return self.find_scan_by_ID(scanID=self.current_scanID[0])

    @property
    def current_scanID(self) -> Optional(str):
        """get the current scanID"""
        if self.current_scan_info is None:
            return None
        return self.current_scan_info.get("scanID")

    @threadlocked
    def find_scan_by_ID(self, scanID: str) -> Optional(ScanItem):
        """find a scan item based on its scanID"""
        for scan in self.storage:
            if scanID == scan.scanID:
                return scan
        return None

    def update_with_scan_status(self, scan_status: BECMessage.ScanStatusMessage) -> None:
        """update scan item in storage with a new ScanStatusMessage"""

        scanID = scan_status.content["scanID"]
        if not scanID:
            return

        scan_number = scan_status.content["info"].get("scan_number")
        if scan_number:
            self.last_scan_number = scan_number

        while True:
            scan_item = self.find_scan_by_ID(scanID=scan_status.content["scanID"])
            if scan_item:
                break
            time.sleep(0.1)

        # update timestamps
        if scan_status.content.get("status") == "open":
            scan_item.start_time = scan_status.content.get("timestamp")
        elif scan_status.content.get("status") == "closed":
            scan_item.end_time = scan_status.content.get("timestamp")

        # update status message
        scan_item.status = scan_status.content.get("status")

        # update total number of points
        if scan_status.content["info"].get("num_points"):
            scan_item.num_points = scan_status.content["info"].get("num_points")

        # update scan number
        if scan_item.scan_number is None:
            scan_item.scan_number = scan_number

        # add scan report info
        scan_item.scan_report_instructions = scan_status.content["info"].get(
            "scan_report_instructions"
        )

        # add scan def id
        scan_def_id = scan_status.content["info"].get("scan_def_id")
        if scan_def_id:
            if scan_status.content.get("status") != "open":
                scan_item.open_scan_defs.remove(scan_def_id)
            else:
                scan_item.open_scan_defs.add(scan_def_id)

        # add queue group
        scan_item.open_queue_group = scan_status.content["info"].get("queue_group")

        # run status callbacks
        scan_item.emit_status(scan_status)

    def add_scan_segment(self, scan_msg: BECMessage.ScanMessage) -> None:
        """update a scan item with a new scan segment"""
        logger.info(
            f"Received scan segment {scan_msg.content['point_id']} for scan {scan_msg.metadata['scanID']}: "
        )
        while True:
            with self._lock:
                for scan_item in self.storage:
                    if scan_item.scanID == scan_msg.metadata["scanID"]:
                        scan_item.data[scan_msg.content["point_id"]] = scan_msg
                        scan_item.emit_data(scan_msg)
                        return
            time.sleep(0.01)

    @threadlocked
    def add_scan_item(self, queueID: str, scan_number: list, scanID: list, status: str):
        """append new scan item to scan storage"""
        self.storage.append(ScanItem(self.scan_manager, queueID, scan_number, scanID, status))

    @threadlocked
    def update_with_queue_status(self, queue_msg: BECMessage.ScanQueueStatusMessage):
        """create new scan items based on their existence in the queue info"""
        queue_info = queue_msg.content["queue"]["primary"].get("info")
        for queue_item in queue_info:
            # append = True
            # for scan_obj in self.storage:
            #     if len(set(scan_obj.scanID) & set(queue_item["scanID"])) > 0:
            #         append = False
            if not any(queue_item["is_scan"]):
                continue

            for ii, scan in enumerate(queue_item["scanID"]):
                if self.find_scan_by_ID(scan):
                    continue

                logger.debug(f"Appending new scan: {queue_item}")
                self.add_scan_item(
                    queueID=queue_item["queueID"],
                    scan_number=queue_item["scan_number"][ii],
                    scanID=queue_item["scanID"][ii],
                    status=queue_item["status"],
                )
