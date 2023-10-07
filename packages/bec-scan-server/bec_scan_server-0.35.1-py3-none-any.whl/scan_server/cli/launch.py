import argparse
import threading

import scan_server
from bec_lib.core import RedisConnector, ServiceConfig, bec_logger

logger = bec_logger.logger
bec_logger.level = bec_logger.LOGLEVEL.INFO


def main():
    """
    Launch the scan server.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--config",
        default="",
        help="path to the config file",
    )
    clargs = parser.parse_args()
    config_path = clargs.config

    config = ServiceConfig(config_path)

    bec_server = scan_server.scan_server.ScanServer(
        config=config,
        connector_cls=RedisConnector,
    )
    try:
        event = threading.Event()
        # pylint: disable=E1102
        logger.success("Started ScanServer")
        event.wait()
    except KeyboardInterrupt as e:
        bec_server.shutdown()
        event.set()
        raise e
