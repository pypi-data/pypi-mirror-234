from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List

import numpy as np
from bec_lib.core import BECMessage, DeviceManagerBase, MessageEndpoints

from bec_client.progressbar import DeviceProgressBar

from .utils import LiveUpdatesBase, check_alarms

if TYPE_CHECKING:
    from bec_client.bec_client import BECClient


class ReadbackDataMixin:
    def __init__(self, device_manager: DeviceManagerBase, devices) -> None:
        self.device_manager = device_manager
        self.devices = devices

    def get_device_values(self):
        """get the current device values"""
        return [
            self.device_manager.devices[dev].read(cached=True, use_readback=True).get("value")
            for dev in self.devices
        ]

    def get_request_done_msgs(self):
        """get all request-done messages"""
        pipe = self.device_manager.producer.pipeline()
        for dev in self.devices:
            self.device_manager.producer.get(MessageEndpoints.device_req_status(dev), pipe)
        return pipe.execute()

    def wait_for_RID(self, request):
        """wait for the readback's metadata to match the request ID"""
        while True:
            msgs = [
                BECMessage.DeviceMessage.loads(
                    self.device_manager.producer.get(MessageEndpoints.device_readback(dev))
                )
                for dev in self.devices
            ]
            if all(msg.metadata.get("RID") == request.metadata["RID"] for msg in msgs if msg):
                break
            check_alarms(self.device_manager.parent)


class LiveUpdatesReadbackProgressbar(LiveUpdatesBase):
    """Live feedback on motor movements using a progressbar.

    Args:
        dm (DeviceManagerBase): device_manager
        request (ScanQueueMessage): request that should be monitored

    """

    def __init__(
        self,
        bec: BECClient,
        report_instruction: List = None,
        request: BECMessage.ScanQueueMessage = None,
        callbacks: List[Callable] = None,
    ) -> None:
        super().__init__(
            bec, report_instruction=report_instruction, request=request, callbacks=callbacks
        )
        if report_instruction:
            self.devices = report_instruction["readback"]["devices"]
        else:
            self.devices = list(request.content["parameter"]["args"].keys())

    async def core(self):
        data_source = ReadbackDataMixin(self.bec.device_manager, self.devices)
        start_values = data_source.get_device_values()
        await self.wait_for_request_acceptance()
        data_source.wait_for_RID(self.request)
        if self.report_instruction:
            self.devices = self.report_instruction["readback"]["devices"]
            target_values = self.report_instruction["readback"]["end"]

            start_instr = self.report_instruction["readback"].get("start")
            if start_instr:
                start_values = self.report_instruction["readback"]["start"]
            data_source = ReadbackDataMixin(self.bec.device_manager, self.devices)
        else:
            target_values = [
                x for xs in self.request.content["parameter"]["args"].values() for x in xs
            ]
            if self.request.content["parameter"]["kwargs"].get("relative"):
                target_values = np.asarray(target_values) + np.asarray(start_values)

        with DeviceProgressBar(
            self.devices, start_values=start_values, target_values=target_values
        ) as progress:
            req_done = False
            while not progress.finished or not req_done:
                check_alarms(self.bec)

                values = data_source.get_device_values()
                progress.update(values=values)

                req_done_msgs = data_source.get_request_done_msgs()
                msgs = [BECMessage.DeviceReqStatusMessage.loads(msg) for msg in req_done_msgs]
                request_ids = [
                    msg.metadata["RID"] if (msg and msg.metadata.get("RID")) else None
                    for msg in msgs
                ]
                if set(request_ids) != set([self.request.metadata["RID"]]):
                    await progress.sleep()
                    continue

                req_done = True
                for dev, msg in zip(self.devices, msgs):
                    if not msg:
                        continue
                    if msg.content.get("success", False):
                        progress.set_finished(dev)

    async def run(self):
        await self.core()
