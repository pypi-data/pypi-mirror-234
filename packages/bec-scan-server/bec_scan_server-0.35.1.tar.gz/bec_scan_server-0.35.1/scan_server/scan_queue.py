from __future__ import annotations

import collections
import functools
import threading
import time
import traceback
import uuid
from enum import Enum
from typing import List, Optional, Union

from rich.console import Console
from rich.table import Table

from bec_lib.core import Alarms, BECMessage, MessageEndpoints, bec_logger, threadlocked

from .errors import LimitError, ScanAbortion
from .scan_assembler import ScanAssembler
from .scans import ScanBase

logger = bec_logger.logger


def requires_queue(fcn):
    """Decorator to ensure that the requested queue exists."""

    @functools.wraps(fcn)
    def wrapper(self, *args, queue="primary", **kwargs):
        if queue not in self.queues:
            self.add_queue(queue)
        return fcn(self, *args, queue=queue, **kwargs)

    return wrapper


class InstructionQueueStatus(Enum):
    STOPPED = -1
    PENDING = 0
    IDLE = 1
    PAUSED = 2
    DEFERRED_PAUSE = 3
    RUNNING = 4
    COMPLETED = 5


class ScanQueueStatus(Enum):
    PAUSED = 0
    RUNNING = 1


class QueueManager:
    # pylint: disable=too-many-instance-attributes
    def __init__(self, parent) -> None:
        self.parent = parent
        self.connector = parent.connector
        self.producer = parent.producer
        self.num_queues = 1
        self.key = ""
        self.queues = {}
        self._start_scan_queue_consumer()
        self._lock = threading.RLock()

    def add_to_queue(self, scan_queue: str, msg: BECMessage.ScanQueueMessage, position=-1) -> None:
        """Add a new ScanQueueMessage to the queue.

        Args:
            scan_queue (str): the queue that should receive the new message
            msg (BECMessage.ScanQueueMessage): ScanQueueMessage

        """
        try:
            self.add_queue(scan_queue)
            self.queues[scan_queue].insert(msg, position=position)
        # pylint: disable=broad-except
        except Exception as exc:
            if len(exc.args) > 0:
                content = exc.args[0]
            else:
                content = ""
            logger.error(content)
            self.connector.raise_alarm(
                severity=Alarms.MAJOR,
                source=msg.content,
                content=content,
                alarm_type=exc.__class__.__name__,
                metadata=msg.metadata,
            )

    @threadlocked
    def add_queue(self, queue_name: str) -> None:
        """add a new queue to the queue manager"""
        if queue_name not in self.queues:
            self.queues[queue_name] = ScanQueue(self, queue_name=queue_name)
            self.queues[queue_name].start_worker()

    def _start_scan_queue_consumer(self) -> None:
        self._scan_queue_consumer = self.connector.consumer(
            MessageEndpoints.scan_queue_insert(),
            cb=self._scan_queue_callback,
            parent=self,
        )
        self._scan_queue_modification_consumer = self.connector.consumer(
            MessageEndpoints.scan_queue_modification(),
            cb=self._scan_queue_modification_callback,
            parent=self,
        )
        self._scan_queue_consumer.start()
        self._scan_queue_modification_consumer.start()

    @staticmethod
    def _scan_queue_callback(msg, parent, **_kwargs) -> None:
        scan_msg = BECMessage.ScanQueueMessage.loads(msg.value)
        logger.info(f"Receiving scan: {scan_msg.content}")
        # instructions = parent.scan_assembler.assemble_device_instructions(scan_msg)
        queue = scan_msg.content.get("queue", "primary")
        parent.add_to_queue(queue, scan_msg)
        parent.send_queue_status()

    @staticmethod
    def _scan_queue_modification_callback(msg, parent, **_kwargs):
        scan_mod_msg = BECMessage.ScanQueueModificationMessage.loads(msg.value)
        logger.info(f"Receiving scan modification: {scan_mod_msg.content}")
        if scan_mod_msg:
            parent.scan_interception(scan_mod_msg)
            parent.send_queue_status()

    @threadlocked
    def scan_interception(self, scan_mod_msg: BECMessage.ScanQueueModificationMessage) -> None:
        """handle a scan interception by compiling the requested method name and forwarding the request.

        Args:
            scan_mod_msg (BECMessage.ScanQueueModificationMessage): ScanQueueModificationMessage

        """
        action = scan_mod_msg.content["action"]
        parameter = scan_mod_msg.content["parameter"]
        getattr(self, f"set_{action}")(scanID=scan_mod_msg.content["scanID"], parameter=parameter)

    @requires_queue
    def set_pause(self, scanID=None, queue="primary", parameter: dict = None) -> None:
        # pylint: disable=unused-argument
        """pause the queue and the currenlty running instruction queue"""
        self.queues[queue].status = ScanQueueStatus.PAUSED
        self.queues[queue].worker_status = InstructionQueueStatus.PAUSED

    @requires_queue
    def set_deferred_pause(self, scanID=None, queue="primary", parameter: dict = None) -> None:
        # pylint: disable=unused-argument
        """pause the queue but continue with the currently running instruction queue until the next checkpoint"""
        self.queues[queue].status = ScanQueueStatus.PAUSED
        self.queues[queue].worker_status = InstructionQueueStatus.DEFERRED_PAUSE

    @requires_queue
    def set_continue(self, scanID=None, queue="primary", parameter: dict = None) -> None:
        # pylint: disable=unused-argument
        """continue with the currently scheduled queue and instruction queue"""
        self.queues[queue].status = ScanQueueStatus.RUNNING
        self.queues[queue].worker_status = InstructionQueueStatus.RUNNING

    @requires_queue
    def set_abort(self, scanID=None, queue="primary", parameter: dict = None) -> None:
        """abort the scan and remove it from the queue. This will leave the queue in a paused state after the cleanup"""
        if self.queues[queue].queue:
            self.queues[queue].status = ScanQueueStatus.PAUSED
        self.queues[queue].worker_status = InstructionQueueStatus.STOPPED
        # self.queues[queue].remove_queue_item(scanID=scanID)

    @requires_queue
    def set_halt(self, scanID=None, queue="primary", parameter: dict = None) -> None:
        """abort the scan and do not perform any cleanup routines"""
        instruction_queue = self.queues[queue].active_instruction_queue
        if instruction_queue:
            instruction_queue.return_to_start = False
        self.set_abort(scanID=scanID, queue=queue)

    @requires_queue
    def set_clear(self, scanID=None, queue="primary", parameter: dict = None) -> None:
        # pylint: disable=unused-argument
        """pause the queue and clear all its elements"""
        self.queues[queue].status = ScanQueueStatus.PAUSED
        self.queues[queue].worker_status = InstructionQueueStatus.STOPPED
        self.queues[queue].clear()

    @requires_queue
    def set_restart(self, scanID=None, queue="primary", parameter: dict = None) -> None:
        """abort and restart the currently running scan. The active scan will be aborted."""
        if not scanID:
            scanID = self._get_active_scanID(queue)
        if not scanID:
            return
        if isinstance(scanID, list):
            scanID = scanID[0]
        self.queues[queue].status = ScanQueueStatus.PAUSED
        self.queues[queue].worker_status = InstructionQueueStatus.STOPPED
        self._lock.release()
        instruction_queue = self._wait_for_queue_to_appear_in_history(scanID, queue)
        self._lock.acquire()
        scan_msg = instruction_queue.scan_msgs[0]
        RID = parameter.get("RID")
        if RID:
            scan_msg.metadata["RID"] = RID
        self.add_to_queue(queue, scan_msg, 0)

    def _get_active_scanID(self, queue):
        if len(self.queues[queue].queue) == 0:
            return None
        if self.queues[queue].queue[0].active_request_block is None:
            return None
        return self.queues[queue].queue[0].active_request_block.scanID

    def _wait_for_queue_to_appear_in_history(self, scanID, queue):
        timeout_time = 10
        elapsed_time = 0
        while True:
            if elapsed_time > timeout_time:
                raise TimeoutError(
                    f"Scan {scanID} did not appear in history within {timeout_time}s"
                )
            elapsed_time += 0.1
            history = self.queues[queue].history_queue
            if len(history) == 0:
                time.sleep(0.1)
                continue
            if not scanID in history[-1].scanID:
                time.sleep(0.1)
                continue

            if len(self.queues[queue].queue) > 0 and scanID in self.queues[queue].queue[0].scanID:
                time.sleep(0.1)
                continue
            return history[-1]

    @threadlocked
    def send_queue_status(self) -> None:
        """send the current queue to redis"""
        queue_export = self.export_queue()
        logger.info("New scan queue:")
        for queue in self.describe_queue():
            logger.info(f"\n {queue}")
        self.producer.set_and_publish(
            MessageEndpoints.scan_queue_status(),
            BECMessage.ScanQueueStatusMessage(queue=queue_export).dumps(),
        )

    def describe_queue(self) -> list:
        """create a rich.table description of the current scan queue"""
        queue_tables = []
        console = Console()
        for queue_name, scan_queue in self.queues.items():
            table = Table(title=f"{queue_name} queue / {scan_queue.status}")
            table.add_column("queueID", justify="center")
            table.add_column("scanID", justify="center")
            table.add_column("is_scan", justify="center")
            table.add_column("type", justify="center")
            table.add_column("scan_number", justify="center")
            table.add_column("IQ status", justify="center")

            queue = list(scan_queue.queue)  # local ref for thread safety
            for instruction_queue in queue:
                table.add_row(
                    instruction_queue.queue_id,
                    ", ".join([str(s) for s in instruction_queue.scanID]),
                    ", ".join([str(s) for s in instruction_queue.is_scan]),
                    ", ".join([msg.content["scan_type"] for msg in instruction_queue.scan_msgs]),
                    ", ".join([str(s) for s in instruction_queue.scan_number]),
                    str(instruction_queue.status.name),
                )
            with console.capture() as capture:
                console.print(table)
            queue_tables.append(capture.get())

        return queue_tables

    def export_queue(self) -> dict:
        """extract the queue info from the queue"""
        queue_export = {}
        for queue_name, scan_queue in self.queues.items():
            queue_info = []
            instruction_queues = list(scan_queue.queue)  # local ref for thread safety
            for instruction_queue in instruction_queues:
                queue_info.append(instruction_queue.describe())
            queue_export[queue_name] = {"info": queue_info, "status": scan_queue.status.name}
        return queue_export

    def shutdown(self):
        """shutdown the queue"""
        for queue in self.queues.values():
            queue.signal_event.set()


class ScanQueue:
    """The ScanQueue manages a queue of InstructionQueues.
    While for most scenarios a single ScanQueue is sufficient,
    multiple ScanQueues can be used to run experiments in parallel.
    The default ScanQueue is always "primary".

    Raises:
        StopIteration: _description_
        StopIteration: _description_

    """

    MAX_HISTORY = 100
    DEFAULT_QUEUE_STATUS = ScanQueueStatus.RUNNING

    def __init__(
        self,
        queue_manager: QueueManager,
        queue_name="primary",
        instruction_queue_item_cls: InstructionQueueItem = None,
    ) -> None:
        self.queue = collections.deque()
        self.queue_name = queue_name
        self.history_queue = collections.deque(maxlen=self.MAX_HISTORY)
        self.active_instruction_queue = None
        self.queue_manager = queue_manager
        self._instruction_queue_item_cls = (
            instruction_queue_item_cls
            if instruction_queue_item_cls is not None
            else InstructionQueueItem
        )
        # self.open_instruction_queue = None
        self._status = self.DEFAULT_QUEUE_STATUS
        self.signal_event = threading.Event()
        self.scan_worker = None
        self.init_scan_worker()

    def init_scan_worker(self):
        """init the scan worker"""
        from .scan_worker import ScanWorker

        self.scan_worker = ScanWorker(parent=self.queue_manager.parent, queue_name=self.queue_name)

    def start_worker(self):
        """start the scan worker"""
        self.scan_worker.start()

    @property
    def worker_status(self) -> Union[None, InstructionQueueStatus]:
        """current status of the instruction queue"""
        if len(self.queue) > 0:
            return self.queue[0].status
        return None

    @worker_status.setter
    def worker_status(self, val: InstructionQueueStatus):
        if len(self.queue) > 0:
            self.queue[0].status = val

    @property
    def status(self):
        """current status of the queue"""
        return self._status

    @status.setter
    def status(self, val: ScanQueueStatus):
        self._status = val
        self.queue_manager.send_queue_status()

    def remove_queue_item(self, scanID: str) -> None:
        """remove a queue item from the queue"""
        if not scanID:
            return
        remove = []
        for queue in self.queue:
            if len(set(scanID) & set(queue.scanID)) > 0:
                remove.append(queue)
        if remove:
            for rmv in remove:
                self.queue.remove(rmv)

    def clear(self):
        """clear the queue"""
        self.queue.clear()
        self.active_instruction_queue = None

    def __iter__(self):
        return self

    def __next__(self):
        while not self.signal_event.is_set():
            try:
                if self.active_instruction_queue is not None and len(self.queue) > 0:
                    self.queue.popleft()
                    self.queue_manager.send_queue_status()

                if self.status != ScanQueueStatus.PAUSED:
                    if len(self.queue) == 0:
                        self.active_instruction_queue = None
                        time.sleep(0.1)
                        continue

                    self.active_instruction_queue = self.queue[0]
                    self.history_queue.append(self.active_instruction_queue)
                    return self.active_instruction_queue

                while self.status == ScanQueueStatus.PAUSED:
                    if len(self.queue) == 0:
                        # we don't need to pause if there is no scan enqueued
                        self.status = ScanQueueStatus.RUNNING
                    time.sleep(0.1)

                self.active_instruction_queue = self.queue[0]
                self.history_queue.append(self.active_instruction_queue)
                # self.active_instruction_queue
                return self.active_instruction_queue

            except IndexError:
                time.sleep(0.01)

    def insert(self, msg: BECMessage.ScanQueueMessage, position=-1, **_kwargs):
        """insert a new message to the queue"""
        target_group = msg.metadata.get("queue_group")
        scan_def_id = msg.metadata.get("scan_def_id")
        instruction_queue = None
        queue_exists = False
        if scan_def_id is not None:
            instruction_queue = self.get_queue_item(scan_def_id=scan_def_id)
            if instruction_queue is not None:
                queue_exists = True
        elif target_group is not None:
            instruction_queue = self.get_queue_item(group=target_group)
            if instruction_queue is not None:
                queue_exists = True
        if not queue_exists:
            # create new queue element (InstructionQueueItem)
            instruction_queue = self._instruction_queue_item_cls(
                parent=self,
                assembler=self.queue_manager.parent.scan_assembler,
                worker=self.scan_worker,
            )
        instruction_queue.append_scan_request(msg)
        if not queue_exists:
            instruction_queue.queue_group = target_group
            if position == -1:
                self.queue.append(instruction_queue)
                return
            self.queue.insert(position, instruction_queue)

    def get_queue_item(self, group=None, scan_def_id=None):
        """get a queue item based on its group or scan_def_id"""
        if scan_def_id is not None:
            for instruction_queue in self.queue:
                if scan_def_id in instruction_queue.queue.scan_def_ids:
                    return instruction_queue
        if group is not None:
            for instruction_queue in self.queue:
                if instruction_queue.queue_group == group:
                    return instruction_queue

        return None

    def abort(self) -> None:
        """abort the current queue item"""
        if self.active_instruction_queue is not None:
            self.active_instruction_queue.abort()

    def get_scan(self, scanID: str) -> Union[None, InstructionQueueItem]:
        """get the instruction queue item based on its scanID"""
        queue_found = None
        for queue in self.history_queue + self.queue:
            if queue.scanID == scanID:
                queue_found = queue
                return queue_found
        return queue_found


class RequestBlock:
    def __init__(self, msg, assembler: ScanAssembler, parent=None) -> None:
        self.instructions = None
        self.scan = None
        self.scan_motors = []
        self.readout_priority = {}
        self.msg = msg
        self.RID = msg.metadata["RID"]
        self.scan_assembler = assembler
        self.is_scan = False
        self.scanID = None
        self._scan_number = None
        self.parent = parent
        self._assemble()
        self.scan_report_instructions = []

    def _assemble(self):
        self.scan = self.scan_assembler.assemble_device_instructions(self.msg)
        self.is_scan = isinstance(self.scan, ScanBase)
        self.scan = self.scan_assembler.assemble_device_instructions(self.msg)
        self.instructions = self.scan.run()
        if (self.is_scan or self.scan_def_id is not None) and self.scanID is None:
            self.scanID = str(uuid.uuid4())
        if self.scan.caller_args:
            self.scan_motors = self.scan.scan_motors
        self.readout_priority = self.scan.readout_priority

    @property
    def scan_def_id(self):
        return self.msg.metadata.get("scan_def_id")

    @property
    def metadata(self):
        return self.msg.metadata

    @property
    def scan_number(self):
        """get the predicted scan number"""
        if not self.is_scan:
            return None
        if self._scan_number is not None:
            return self._scan_number
        return self._scan_server_scan_number + self.scanIDs_head()

    @property
    def _scan_server_scan_number(self):
        return self.parent.scan_queue.queue_manager.parent.scan_number

    def assign_scan_number(self) -> None:
        """assign and fix the current scan number prediction"""
        if not self.is_scan:
            return None
        self._scan_number = self._scan_server_scan_number + self.scanIDs_head()
        return None

    def scanIDs_head(self) -> int:
        """calculate the scanID offset in the queue for the current request block"""
        offset = 0
        for queue in self.parent.scan_queue.queue:
            if queue.status == InstructionQueueStatus.COMPLETED:
                continue
            if queue.queue_id != self.parent.instruction_queue.queue_id:
                offset += len([scanID for scanID in queue.scanID if scanID])
            else:
                for scanID in queue.scanID:
                    if scanID == self.scanID:
                        return offset
                    if scanID:
                        offset += 1
                return offset
        return offset

    def describe(self):
        """prepare a dictionary that summarizes the request block"""
        return {
            "msg": self.msg.dumps(),
            "RID": self.RID,
            "scan_motors": self.scan_motors,
            "readout_priority": self.readout_priority,
            "is_scan": self.is_scan,
            "scan_number": self.scan_number,
            "scanID": self.scanID,
            "metadata": self.msg.metadata,
            "content": self.msg.content,
            "report_instructions": self.scan_report_instructions,
        }


class RequestBlockQueue:
    def __init__(self, instruction_queue, assembler) -> None:
        self.request_blocks_queue = collections.deque()
        self.request_blocks = []
        self.instruction_queue = instruction_queue
        self.scan_queue = instruction_queue.parent
        self.assembler = assembler
        self.active_rb = None
        self.scan_def_ids = {}

    @property
    def scanID(self) -> List[str]:
        """get the scanIDs for all request blocks"""
        return [rb.scanID for rb in self.request_blocks]

    @property
    def is_scan(self) -> List[bool]:
        """check if the request blocks describe scans"""
        return [rb.is_scan for rb in self.request_blocks]

    @property
    def scan_number(self) -> List[int]:
        """get the list of scan numbers for all request blocks"""
        return [rb.scan_number for rb in self.request_blocks]

    def append(self, msg: BECMessage.ScanQueueMessage) -> None:
        """append a new scan queue message"""
        request_block = RequestBlock(msg, self.assembler, parent=self)
        self._update_scan_def_id(request_block)
        self.append_request_block(request_block)

    def _update_scan_def_id(self, request_block: RequestBlock):
        if "scan_def_id" not in request_block.msg.metadata:
            return
        scan_def_id = request_block.msg.metadata["scan_def_id"]
        if scan_def_id in self.scan_def_ids:
            request_block.scanID = self.scan_def_ids[scan_def_id]["scanID"]
        else:
            self.scan_def_ids[scan_def_id] = {"scanID": request_block.scanID, "pointID": 0}

    def append_request_block(self, request_block: RequestBlock) -> None:
        """append a new request block to the queue"""
        self.request_blocks_queue.append(request_block)
        self.request_blocks.append(request_block)

    def flush_request_blocks(self) -> None:
        """clear all request blocks from the queue"""
        self.request_blocks = []
        self.request_blocks_queue.clear()

    def _pull_request_block(self):
        if self.active_rb is not None:
            return
        if len(self.request_blocks_queue) == 0:
            raise StopIteration
        self.active_rb = self.request_blocks_queue.popleft()
        self._update_point_id(self.active_rb)

        if self.active_rb.is_scan:
            self.active_rb.assign_scan_number()

    def _update_point_id(self, request_block: RequestBlock):
        if request_block.scan_def_id not in self.scan_def_ids:
            return
        if hasattr(request_block.scan, "pointID"):
            request_block.scan.pointID = self.scan_def_ids[request_block.scan_def_id]["pointID"]

    def increase_scan_number(self) -> None:
        """increase the scan number counter"""
        rbl = self.active_rb
        if not rbl.is_scan and rbl.scan_def_id is None:
            return
        if rbl.scan_def_id is None or rbl.msg.content["scan_type"] == "close_scan_def":
            self.scan_queue.queue_manager.parent.scan_number += 1
            if not rbl.msg.metadata.get("dataset_id_on_hold"):
                self.scan_queue.queue_manager.parent.dataset_number += 1
        return

    def __iter__(self):
        return self

    def __next__(self):
        self._pull_request_block()
        try:
            return next(self.active_rb.instructions)
        except StopIteration:
            if self.active_rb.scan_def_id in self.scan_def_ids:
                pointID = getattr(self.active_rb.scan, "pointID", None)
                if pointID is not None:
                    self.scan_def_ids[self.active_rb.scan_def_id]["pointID"] = pointID
            self.increase_scan_number()
            self.active_rb = None
            self._pull_request_block()
            return next(self.active_rb.instructions)
        except LimitError as limit_error:
            self.scan_queue.queue_manager.connector.raise_alarm(
                severity=Alarms.MAJOR,
                source=self.active_rb.msg.content,
                content=limit_error.args[0],
                alarm_type=limit_error.__class__.__name__,
                metadata={},
            )
            raise ScanAbortion from limit_error
        # pylint: disable=broad-except
        except Exception as exc:
            content = traceback.format_exc()
            logger.error(content)
            self.scan_queue.queue_manager.connector.raise_alarm(
                severity=Alarms.MAJOR,
                source=self.active_rb.msg.content,
                content=content,
                alarm_type=exc.__class__.__name__,
                metadata={},
            )
            raise ScanAbortion from exc


class InstructionQueueItem:
    """The InstructionQueueItem contains and manages the request blocks for a queue item.
    While an InstructionQueueItem can be comprised of multiple requests,
    it will always have at max one scan_number / scanID.

    Raises:
        StopIteration: _description_
        StopIteration: _description_

    Returns:
        _type_: _description_
    """

    def __init__(self, parent: ScanQueue, assembler: ScanAssembler, worker) -> None:
        self.instructions = []
        self.parent = parent
        self.queue = RequestBlockQueue(instruction_queue=self, assembler=assembler)
        self.producer = self.parent.queue_manager.producer
        self._is_scan = False
        self.is_active = False  # set to true while a worker is processing the instructions
        self.completed = False
        self.deferred_pause = True
        self.queue_group = None
        self.queue_group_is_closed = False
        self.subqueue = iter([])
        self.queue_id = str(uuid.uuid4())
        self.scan_msgs = []
        self.scan_assembler = assembler
        self.worker = worker
        self.stopped = False
        self._status = InstructionQueueStatus.PENDING
        self._return_to_start = None

    @property
    def scan_number(self) -> List[int]:
        """get the scan numbers for the elements in this instruction queue"""
        return self.queue.scan_number

    @property
    def status(self) -> InstructionQueueStatus:
        """get the status of the instruction queue"""
        return self._status

    @status.setter
    def status(self, val: InstructionQueueStatus) -> None:
        """update the status of the instruction queue. By doing so, it will
        also update its worker and publish the updated queue."""
        if val == InstructionQueueStatus.PENDING:
            print("stop!")
        self._status = val
        self.worker.status = val
        self.parent.queue_manager.send_queue_status()

    @property
    def active_request_block(self) -> RequestBlock:
        """get the currently active request block"""
        return self.queue.active_rb

    @property
    def scan_macros_complete(self) -> bool:
        """check if the scan macro has been completed"""
        return len(self.queue.scan_def_ids) == 0

    @property
    def scanID(self) -> List[str]:
        """get the scanIDs"""
        return self.queue.scanID

    @property
    def is_scan(self) -> List[bool]:
        """check whether the InstructionQueue contains scan."""
        return self.queue.is_scan

    def abort(self) -> None:
        """abort and clear all the instructions from the instruction queue"""
        self.instructions = iter([])

    def append_scan_request(self, msg):
        """append a scan message to the instruction queue"""
        self.scan_msgs.append(msg)
        self.queue.append(msg)

    def set_active(self):
        """change the instruction queue status to RUNNING"""
        if self.status == InstructionQueueStatus.PENDING:
            self.status = InstructionQueueStatus.RUNNING

    @property
    def return_to_start(self) -> bool:
        """whether or not to return to the start position after scan abortion"""
        if self._return_to_start is not None:
            return self._return_to_start
        if self.active_request_block:
            return self.active_request_block.scan.return_to_start_after_abort
        return False

    @return_to_start.setter
    def return_to_start(self, val: bool) -> bool:
        self._return_to_start = val

    def describe(self):
        """description of the instruction queue"""
        request_blocks = [rb.describe() for rb in self.queue.request_blocks]
        content = {
            "queueID": self.queue_id,
            "scanID": self.scanID,
            "is_scan": self.is_scan,
            "request_blocks": request_blocks,
            "scan_number": self.scan_number,
            "status": self.status.name,
            "active_request_block": self.active_request_block.describe()
            if self.active_request_block
            else None,
        }
        return content

    def append_to_queue_history(self):
        """append a new queue item to the redis history buffer"""
        msg = BECMessage.ScanQueueHistoryMessage(
            status=self.status.name, queueID=self.queue_id, info=self.describe()
        )
        self.parent.queue_manager.producer.lpush(
            MessageEndpoints.scan_queue_history(), msg.dumps(), max_size=100
        )

    def __iter__(self):
        return self

    def _set_finished(self, raise_stopiteration=True):
        self.completed = True
        if raise_stopiteration:
            raise StopIteration

    def _get_next(
        self, queue="instructions", raise_stopiteration=True
    ) -> Optional(BECMessage.DeviceInstructionMessage):
        try:
            instr = next(self.queue)
            # instr = next(self.__getattribute__(queue))
            if not instr:
                return None
            if instr.content.get("action") == "close_scan_group":
                self.queue_group_is_closed = True
                raise StopIteration
            if instr.content.get("action") == "close_scan_def":
                scan_def_id = instr.metadata.get("scan_def_id")
                if scan_def_id in self.queue.scan_def_ids:
                    self.queue.scan_def_ids.pop(scan_def_id)

            instr.metadata["scanID"] = self.queue.active_rb.scanID
            instr.metadata["queueID"] = self.queue_id
            self.set_active()
            return instr

        except StopIteration:
            if not self.scan_macros_complete:
                logger.info(
                    f"Waiting for new instructions or scan macro to be closed (scan def ids: {self.queue.scan_def_ids})"
                )
                time.sleep(0.1)
            elif self.queue_group is not None and not self.queue_group_is_closed:
                self.queue.active_rb = None
                self.parent.queue_manager.send_queue_status()
                logger.info(
                    f"Waiting for new instructions or queue group to be closed (group id: {self.queue_group})"
                )
                time.sleep(0.1)
            else:
                self._set_finished(raise_stopiteration=raise_stopiteration)
        return None

    def __next__(self):
        if self.status in [
            InstructionQueueStatus.RUNNING,
            InstructionQueueStatus.DEFERRED_PAUSE,
            InstructionQueueStatus.PENDING,
        ]:
            return self._get_next()

        while self.status == InstructionQueueStatus.PAUSED:
            return self._get_next(queue="subqueue", raise_stopiteration=False)

        return self._get_next()
