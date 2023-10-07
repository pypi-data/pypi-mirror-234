from __future__ import annotations

import threading
from collections import deque
from typing import TYPE_CHECKING, Deque, Optional

from bec_lib.callback_handler import CallbackHandler
from bec_lib.core import BECMessage, bec_logger, threadlocked

logger = bec_logger.logger


if TYPE_CHECKING:
    from queue_items import QueueItem
    from scan_items import ScanItem
    from scan_manager import ScanManager


class RequestItem:
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        scan_manager: ScanManager,
        requestID: str,
        decision_pending: bool = True,
        scanID: str = None,
        request=None,
        response=None,
        accepted: bool = None,
        **_kwargs,
    ) -> None:
        self.scan_manager = scan_manager
        self.requestID = requestID
        self.request = request
        self.response = response
        self.accepted = accepted
        self._decision_pending = decision_pending
        self._scanID = scanID
        self.callbacks = CallbackHandler()

    def update_with_response(self, response: BECMessage.RequestResponseMessage):
        """update the current request item with a RequestResponseMessage / response message"""
        self.response = response
        self._decision_pending = False
        self.requestID = response.metadata["RID"]
        self.accepted = [response.content["accepted"]]

    def update_with_request(self, request: BECMessage.ScanQueueMessage):
        """update the current request item with a ScanQueueMessage / request message"""
        self.request = request
        self.requestID = request.metadata["RID"]

    @property
    def decision_pending(self) -> bool:
        """indicates whether a decision has been made to accept or decline a scan request"""
        if not self._decision_pending:
            return self._decision_pending

        if self.scan:
            self._decision_pending = False
            self.accepted = [True]
        return self._decision_pending

    @decision_pending.setter
    def decision_pending(self, val: bool) -> None:
        self._decision_pending = val

    @classmethod
    def from_response(cls, scan_manager: ScanManager, response: BECMessage.RequestResponseMessage):
        """initialize a request item from a RequestReponseMessage / response message"""
        scan_req = cls(
            scan_manager=scan_manager,
            requestID=response.metadata["RID"],
            response=response,
            decision_pending=False,
            accepted=[response.content["accepted"]],
        )
        return scan_req

    @classmethod
    def from_request(cls, scan_manager: ScanManager, request: BECMessage.ScanQueueMessage):
        """initialize a request item from a ScanQueueMessage / request message"""
        scan_req = cls(
            scan_manager=scan_manager, requestID=request.metadata["RID"], request=request
        )
        return scan_req

    @property
    def scan(self) -> Optional(ScanItem):
        """get the scan item for the given request item"""
        queue_item = self.scan_manager.queue_storage.find_queue_item_by_requestID(self.requestID)
        if not queue_item:
            return None
        # pylint: disable=protected-access
        request_index = queue_item.requestIDs.index(self.requestID)
        return queue_item.scans[request_index]

    @property
    def queue(self) -> QueueItem:
        """get the queue item for the given request_item"""
        return self.scan_manager.queue_storage.find_queue_item_by_requestID(self.requestID)


class RequestStorage:
    """stores request items"""

    def __init__(self, scan_manager: ScanManager, maxlen=50) -> None:
        self.storage: Deque[RequestItem] = deque(maxlen=maxlen)
        self._lock = threading.RLock()
        self.scan_manager = scan_manager

    @threadlocked
    def find_request_by_ID(self, requestID: str) -> Optional(RequestItem):
        """find a request item based on its requestID"""
        for request in self.storage:
            if request.requestID == requestID:
                return request
        return None

    @threadlocked
    def update_with_response(self, response_msg: BECMessage.RequestResponseMessage) -> None:
        """create or update request item based on a new RequestResponseMessage"""
        request_item = self.find_request_by_ID(response_msg.metadata.get("RID"))
        if request_item:
            request_item.update_with_response(response_msg)
            logger.debug("Scan queue request exists. Updating with response.")
            return

        # it could be that the response arrived before the request
        self.storage.append(RequestItem.from_response(self.scan_manager, response_msg))
        logger.debug("Scan queue request does not exist. Creating from response.")

    @threadlocked
    def update_with_request(self, request_msg: BECMessage.ScanQueueMessage) -> None:
        """create or update request item based on a new ScanQueueMessage (i.e. request message)"""
        if not request_msg.metadata:
            return

        if not request_msg.metadata.get("RID"):
            return

        request_item = self.find_request_by_ID(request_msg.metadata.get("RID"))
        if request_item:
            request_item.update_with_request(request_msg)
            return

        self.storage.append(RequestItem.from_request(self.scan_manager, request_msg))
        return
