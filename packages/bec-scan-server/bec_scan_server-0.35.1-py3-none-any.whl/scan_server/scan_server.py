from __future__ import annotations

from bec_lib.core import Alarms, BECMessage, BECService, BECStatus
from bec_lib.core import DeviceManagerBase as DeviceManager
from bec_lib.core import MessageEndpoints, ServiceConfig, bec_logger
from bec_lib.core.connector import ConnectorBase

from .scan_assembler import ScanAssembler
from .scan_guard import ScanGuard
from .scan_manager import ScanManager
from .scan_queue import QueueManager

logger = bec_logger.logger


class ScanServer(BECService):
    device_manager = None
    queue_manager = None
    scan_guard = None
    scan_server = None
    scan_assembler = None
    scan_manager = None

    def __init__(self, config: ServiceConfig, connector_cls: ConnectorBase):
        super().__init__(config, connector_cls, unique_service=True)
        self.producer = self.connector.producer()
        self._start_scan_manager()
        self._start_queue_manager()
        self._start_device_manager()
        self._start_scan_guard()
        self._start_scan_assembler()
        # self._start_scan_server()
        self._start_alarm_handler()
        self._reset_scan_number()
        self.status = BECStatus.RUNNING

    def _start_device_manager(self):
        self.device_manager = DeviceManager(self.connector)
        self.device_manager.initialize([self.bootstrap_server])

    def _start_scan_manager(self):
        self.scan_manager = ScanManager(parent=self)

    def _start_queue_manager(self):
        self.queue_manager = QueueManager(parent=self)

    def _start_scan_assembler(self):
        self.scan_assembler = ScanAssembler(parent=self)

    def _start_scan_guard(self):
        self.scan_guard = ScanGuard(parent=self)

    def _start_alarm_handler(self):
        self._alarm_consumer = self.connector.consumer(
            MessageEndpoints.alarm(),
            cb=self._alarm_callback,
            parent=self,
        )
        self._alarm_consumer.start()

    def _reset_scan_number(self):
        if self.producer.get(MessageEndpoints.scan_number()) is None:
            self.scan_number = 1
        if self.producer.get(MessageEndpoints.dataset_number()) is None:
            self.dataset_number = 1

    @staticmethod
    def _alarm_callback(msg, parent: ScanServer, **_kwargs):
        msg = BECMessage.AlarmMessage.loads(msg.value)
        queue = msg.metadata.get("queue", "primary")
        if Alarms(msg.content["severity"]) == Alarms.MAJOR:
            # shouldn't this be specific to a single queue?
            parent.queue_manager.set_abort(queue=queue)

    @property
    def scan_number(self) -> int:
        """get the current scan number"""
        return int(self.producer.get(MessageEndpoints.scan_number()))

    @scan_number.setter
    def scan_number(self, val: int):
        """set the current scan number"""
        self.producer.set(MessageEndpoints.scan_number(), val)

    @property
    def dataset_number(self) -> int:
        """get the current dataset number"""
        return int(self.producer.get(MessageEndpoints.dataset_number()))

    @dataset_number.setter
    def dataset_number(self, val: int):
        """set the current dataset number"""
        self.producer.set(MessageEndpoints.dataset_number(), val)

    def shutdown(self) -> None:
        """shutdown the scan server"""

        self.device_manager.shutdown()
        self.queue_manager.shutdown()
