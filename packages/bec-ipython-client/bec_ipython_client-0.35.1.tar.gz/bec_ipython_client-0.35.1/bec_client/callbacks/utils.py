from __future__ import annotations

import abc
import asyncio
import threading
import time
import traceback
from typing import TYPE_CHECKING, Callable, List

from bec_lib.core import Alarms, BECMessage, bec_logger
from bec_lib.request_items import RequestItem

if TYPE_CHECKING:
    from bec_client.bec_client import BECClient

logger = bec_logger.logger


class ScanRequestError(Exception):
    pass


def set_event_delayed(event: threading.Event, delay: int) -> None:
    """Set event with a delay

    Args:
        event (threading.Event): event that should be set
        delay (int): delay time in seconds

    """

    def call_set():
        time.sleep(delay)
        event.set()

    thread = threading.Thread(target=call_set, daemon=True)
    thread.start()


def check_alarms(bec):
    """check for alarms and raise them if needed"""
    bec.alarm_handler.raise_alarms()


class LiveUpdatesBase(abc.ABC):
    def __init__(
        self,
        bec: BECClient,
        report_instruction: dict = None,
        request: BECMessage.ScanQueueMessage = None,
        callbacks: List[Callable] = None,
    ) -> None:
        self.bec = bec
        self.request = request
        self.RID = request.metadata["RID"]
        self.scan_queue_request = None
        self.report_instruction = report_instruction
        if callbacks is None:
            self.callbacks = []
        self.callbacks = callbacks if isinstance(callbacks, list) else [callbacks]

    async def wait_for_request_acceptance(self):
        scan_request = ScanRequestMixin(self.bec, self.RID)
        await scan_request.wait()
        self.scan_queue_request = scan_request.scan_queue_request

    @abc.abstractmethod
    def run(self):
        pass

    def emit_point(self, data: dict, metadata: dict = None):
        for cb in self.callbacks:
            if not cb:
                continue
            try:
                cb(data, metadata=metadata)
            except Exception:
                content = traceback.format_exc()
                logger.warning(f"Failed to run callback function: {content}")


class ScanRequestMixin:
    def __init__(self, bec: BECClient, RID: str) -> None:
        self.bec = bec
        self.request_storage = self.bec.queue.request_storage
        self.RID = RID
        self.scan_queue_request = None

    async def _wait_for_scan_request(self) -> RequestItem:
        """wait for scan queuest"""
        logger.debug("Waiting for request ID")
        start = time.time()
        while self.request_storage.find_request_by_ID(self.RID) is None:
            await asyncio.sleep(0.1)
        logger.debug(f"Waiting for request ID finished after {time.time()-start} s.")
        return self.request_storage.find_request_by_ID(self.RID)

    async def _wait_for_scan_request_decision(self):
        """wait for a scan queuest decision"""
        logger.debug("Waiting for decision")
        start = time.time()
        while self.scan_queue_request.decision_pending:
            await asyncio.sleep(0.1)
        logger.debug(f"Waiting for decision finished after {time.time()-start} s.")

    async def wait(self):
        """wait for the request acceptance"""
        self.scan_queue_request = await self._wait_for_scan_request()

        await self._wait_for_scan_request_decision()
        check_alarms(self.bec)

        while self.scan_queue_request.accepted is None:
            await asyncio.sleep(0.01)

        if not self.scan_queue_request.accepted[0]:
            raise ScanRequestError(
                f"Scan was rejected by the server: {self.scan_queue_request.response.content.get('message')}"
            )

        while self.scan_queue_request.queue is None:
            await asyncio.sleep(0.01)
