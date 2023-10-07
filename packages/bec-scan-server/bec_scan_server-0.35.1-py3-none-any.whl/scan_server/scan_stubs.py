import time
import uuid
from typing import Callable, List, Union

import numpy as np
from bec_lib.core import (
    BECMessage,
    MessageEndpoints,
    ProducerConnector,
    Status,
    bec_logger,
)

from .errors import DeviceMessageError, ScanAbortion

DeviceMsg = BECMessage.DeviceInstructionMessage
logger = bec_logger.logger


class ScanStubs:
    def __init__(self, producer: ProducerConnector, device_msg_callback: Callable = None) -> None:
        self.producer = producer
        self.device_msg_metadata = (
            device_msg_callback if device_msg_callback is not None else lambda: {}
        )

    @staticmethod
    def _exclude_nones(input_dict: dict):
        for key in list(input_dict.keys()):
            if input_dict[key] is None:
                input_dict.pop(key)

    def _device_msg(self, **kwargs):
        """"""
        msg = DeviceMsg(**kwargs)
        msg.metadata = {**self.device_msg_metadata(), **msg.metadata}
        return msg

    def send_rpc_and_wait(self, device: str, func_name: str, *args, **kwargs):
        """Perform an RPC (remote procedure call) on a device and wait for its return value.

        Args:
            device (str): Name of the device
            func_name (str): Function name. The function name will be appended to the device.
            args (tuple): Arguments to pass on to the RPC function
            kwargs (dict): Keyword arguments to pass on to the RPC function

        Raises:
            ScanAbortion: Raised if the RPC's success is False

        Returns:
            any: Return value of the executed rpc function

        Examples:
            >>> send_rpc_and_wait("samx", "controller.my_custom_function")
        """
        rpc_id = str(uuid.uuid4())
        parameter = {
            "device": device,
            "func": func_name,
            "rpc_id": rpc_id,
            "args": args,
            "kwargs": kwargs,
        }
        yield from self.rpc(device=device, parameter=parameter, metadata={"response": True})
        return self._get_from_rpc(rpc_id)

    def _get_from_rpc(self, rpc_id):
        while True:
            msg = self.producer.get(MessageEndpoints.device_rpc(rpc_id))
            if msg:
                break
            time.sleep(0.001)
        msg = BECMessage.DeviceRPCMessage.loads(msg)
        if not msg.content["success"]:
            error = msg.content["out"]
            if isinstance(error, dict) and {"error", "msg", "traceback"}.issubset(
                set(error.keys())
            ):
                error_msg = f"During an RPC, the following error occured:\n{error['error']}: {error['msg']}.\nTraceback: {error['traceback']}\n The scan will be aborted."
            else:
                error_msg = "During an RPC, an error occured"
            raise ScanAbortion(error_msg)

        logger.debug(msg.content.get("out"))
        return_val = msg.content.get("return_val")
        if not isinstance(return_val, dict):
            return return_val
        if return_val.get("type") == "status" and return_val.get("RID"):
            return Status(self.producer, return_val.get("RID"))
        return return_val

    def set_and_wait(self, *, device: List[str], positions: Union[list, np.ndarray]):
        """Set devices to a specific position and wait completion.

        Args:
            device (List[str]): List of device names.
            positions (Union[list, np.ndarray]): Target position.

        """
        if not isinstance(positions, list) and not isinstance(positions, np.ndarray):
            positions = [positions]
        if len(positions) == 0:
            return
        for ind, val in enumerate(device):
            yield from self.set(device=val, value=positions[ind], wait_group="scan_motor")
        yield from self.wait(device=device, wait_type="move", wait_group="scan_motor")

    def read_and_wait(
        self, *, wait_group: str, device: list = None, group: str = None, pointID: int = None
    ):
        """Trigger a reading and wait for completion.

        Args:
            wait_group (str): wait group
            device (list, optional): List of device names. Can be specified instead of group. Defaults to None.
            group (str, optional): Group name of devices. Can be specified instead of device. Defaults to None.
            pointID (int, optional): _description_. Defaults to None.

        """
        self._check_device_and_groups(device, group)
        yield from self.read(device=device, group=group, wait_group=wait_group, pointID=pointID)
        yield from self.wait(device=device, wait_type="read", group=group, wait_group=wait_group)

    def open_scan(
        self,
        *,
        scan_motors: list,
        readout_priority: dict,
        num_pos: int,
        scan_name: str,
        scan_type: str,
        positions=None,
        metadata=None,
    ):
        """Open a new scan.

        Args:
            scan_motors (list): List of scan motors.
            readout_priority (dict): Modification of the readout priority.
            num_pos (int): Number of positions within the scope of this scan.
            positions (list): List of positions for this scan.
            scan_name (str): Scan name.
            scan_type (str): Scan type (e.g. 'step' or 'fly')

        """
        yield self._device_msg(
            device=None,
            action="open_scan",
            parameter={
                "scan_motors": scan_motors,
                "readout_priority": readout_priority,
                "num_points": num_pos,
                "positions": positions,
                "scan_name": scan_name,
                "scan_type": scan_type,
            },
            metadata=metadata,
        )

    def kickoff(self, *, device: str, parameter: dict = None, wait_group="kickoff", metadata=None):
        """Kickoff a fly scan device.

        Args:
            device (str): Device name of flyer.
            parameter (dict, optional): Additional parameters that should be forwarded to the device. Defaults to {}.
        """
        parameter = parameter if parameter is not None else {}
        parameter = {"configure": parameter, "wait_group": wait_group}
        yield self._device_msg(
            device=device,
            action="kickoff",
            parameter=parameter,
            metadata=metadata,
        )

    def complete(self, *, device: str, metadata=None):
        """Complete a fly scan device.

        Args:
            device (str): Device name of flyer.
        """
        yield self._device_msg(
            device=device,
            action="complete",
            parameter={},
            metadata=metadata,
        )

    def get_req_status(self, device: str, RID: str, DIID: int):
        """Check if a device request status matches the given RID and DIID

        Args:
            device (str): device under inspection
            RID (str): request ID
            DIID (int): device instruction ID

        """
        raw_msg = self.producer.get(MessageEndpoints.device_req_status(device))
        if not raw_msg:
            return 0
        msg = BECMessage.DeviceReqStatusMessage.loads(raw_msg)
        matching_RID = msg.metadata.get("RID") == RID
        matching_DIID = msg.metadata.get("DIID") == DIID
        if matching_DIID and matching_RID:
            return 1
        return 0

    def get_device_progress(self, device: str, RID: str):
        """Get reported device progress

        Args:
            device (str): Name of the device
            RID (str): request ID

        """
        raw_msg = self.producer.get(MessageEndpoints.device_progress(device))
        if not raw_msg:
            return None
        msg = BECMessage.DeviceStatusMessage.loads(raw_msg)
        matching_RID = msg.metadata.get("RID") == RID
        if not matching_RID:
            return None
        return msg.content["status"]

    def close_scan(self):
        """Close the scan."""
        yield self._device_msg(device=None, action="close_scan", parameter={})

    def stage(self):
        """Stage all devices"""
        yield self._device_msg(device=None, action="stage", parameter={})

    def unstage(self):
        """Unstage all devices"""
        yield self._device_msg(device=None, action="unstage", parameter={})

    def pre_scan(self):
        """Trigger pre-scan actions on all devices"""
        yield self._device_msg(device=None, action="pre_scan", parameter={})

    def baseline_reading(self):
        """Run the baseline readings."""
        yield self._device_msg(
            device=None,
            action="baseline_reading",
            parameter={},
            metadata={"readout_priority": "baseline"},
        )

    def wait(
        self,
        *,
        wait_type: str,
        device: Union[List[str], str] = None,
        group: str = None,
        wait_group: str = None,
        wait_time: float = None,
    ):
        """Wait for an event.

        Args:
            wait_type (str): wait type
            device (Union[List[str], str], optional): List of device names. Defaults to None.
            group (str, optional): Device group that can be used instead of the device argument. Defaults to None.
            wait_group (str, optional): Wait group. Defaults to None.
            wait_time (float, optional): Wait time (for wait_type="trigger"). Defaults to None.

        """
        self._check_device_and_groups(device, group)
        parameter = {"type": wait_type, "time": wait_time, "group": group, "wait_group": wait_group}
        self._exclude_nones(parameter)
        yield self._device_msg(
            device=device,
            action="wait",
            parameter=parameter,
        )

    def read(
        self,
        *,
        wait_group: str,
        device: list = None,
        pointID: int = None,
        group: str = None,
    ):
        """Read from a device / device group.

        Args:
            wait_group (str): Wait group.
            device (list, optional): Device name. Can be used instead of group. Defaults to None.
            pointID (int, optional): pointID to assign this reading to point within the scan. Defaults to None.
            group (str, optional): Device group. Can be used instead of device. Defaults to None.

        """
        self._check_device_and_groups(device, group)
        parameter = {"group": group, "wait_group": wait_group}
        metadata = {"pointID": pointID}
        self._exclude_nones(parameter)
        self._exclude_nones(metadata)
        yield self._device_msg(
            device=device,
            action="read",
            parameter=parameter,
            metadata=metadata,
        )

    def publish_data_as_read(self, *, device: str, data: dict, pointID: int):
        metadata = {"pointID": pointID}
        yield self._device_msg(
            device=device,
            action="publish_data_as_read",
            parameter={"data": {device: data}},
            metadata=metadata,
        )

    def trigger(self, *, group: str, pointID: int):
        """Trigger a device group

        Args:
            group (str): Device group that should receive the trigger.
            pointID (int): pointID that should be attached to this trigger event.

        """
        yield self._device_msg(
            device=None,
            action="trigger",
            parameter={"group": group},
            metadata={"pointID": pointID},
        )

    def set(self, *, device: str, value: float, wait_group: str, metadata=None):
        """Set the device to a specific value.

        Args:
            device (str): Device name
            value (float): Target value.
            wait_group (str): wait group for this event.

        """
        yield self._device_msg(
            device=device,
            action="set",
            parameter={
                "value": value,
                "wait_group": wait_group,
            },
            metadata=metadata,
        )

    def open_scan_def(self):
        """open a new scan definition"""
        yield self._device_msg(device=None, action="open_scan_def", parameter={})

    def close_scan_def(self):
        """close a scan definition"""
        yield self._device_msg(device=None, action="close_scan_def", parameter={})

    def close_scan_group(self):
        """close a scan group"""
        yield self._device_msg(device=None, action="close_scan_group", parameter={})

    def rpc(self, *, device: str, parameter: dict, metadata=None):
        """Perfrom an RPC (remote procedure call) on a device.

        Args:
            device (str): Device name.
            parameter (dict): parameters used for this rpc instructions.

        """
        yield self._device_msg(
            device=device,
            action="rpc",
            parameter=parameter,
            metadata=metadata,
        )

    def scan_report_instruction(self, instructions: dict):
        """Scan report instructions

        Args:
            instructions (dict): Dict containing the scan report instructions
        """
        yield self._device_msg(
            device=None, action="scan_report_instruction", parameter=instructions
        )

    def _check_device_and_groups(self, device, group):
        if device and group:
            raise DeviceMessageError("Device and device group was specified. Pick one.")
        if device is None and group is None:
            raise DeviceMessageError("Either devices or device groups have to be specified.")
