import traceback

from bec_lib.core import BECMessage, bec_logger

from .errors import ScanAbortion
from .scans import RequestBase, unpack_scan_args

logger = bec_logger.logger


class ScanAssembler:
    """
    ScanAssembler receives scan messages and translates the scan message into device instructions.
    """

    def __init__(self, *, parent):
        self.parent = parent
        self.device_manager = self.parent.device_manager
        self.connector = self.parent.connector
        self.scan_manager = self.parent.scan_manager

    def assemble_device_instructions(self, msg: BECMessage.ScanQueueMessage) -> RequestBase:
        """Assemble the device instructions for a given ScanQueueMessage.
        This will be achieved by calling the specified class (must be a derived class of RequestBase)

        Args:
            msg (BECMessage.ScanQueueMessage): scan queue message for which the instruction should be assembled

        Raises:
            ScanAbortion: Raised if the scan initialization fails.

        Returns:
            RequestBase: Scan instance of the initialized scan class
        """
        scan = msg.content.get("scan_type")
        cls_name = self.scan_manager.available_scans[scan]["class"]
        scan_cls = self.scan_manager.scan_dict[cls_name]

        logger.info(f"Preparing instructions of request of type {scan} / {scan_cls.__name__}")
        try:
            args = unpack_scan_args(msg.content.get("parameter", {}).get("args", []))
            kwargs = msg.content.get("parameter", {}).get("kwargs", {})
            scan_instance = scan_cls(
                *args,
                device_manager=self.device_manager,
                parameter=msg.content.get("parameter"),
                metadata=msg.metadata,
                **kwargs,
            )
            return scan_instance
        except Exception as exc:
            content = traceback.format_exc()
            logger.error(
                f"Failed to initialize the scan class of type {scan_cls.__name__}. {content}"
            )
            raise ScanAbortion from exc
