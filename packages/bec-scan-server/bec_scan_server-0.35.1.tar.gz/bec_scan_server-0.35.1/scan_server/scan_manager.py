import glob
import importlib
import importlib.util
import inspect
import os
from pathlib import Path

import msgpack
from bec_lib.core import MessageEndpoints, bec_logger
from bec_lib.core.signature_serializer import signature_to_dict

from . import scans as ScanServerScans

logger = bec_logger.logger


class ScanManager:
    DEFAULT_PLUGIN_PATH = Path(os.path.dirname(os.path.abspath(__file__)) + "/../../").resolve()

    def __init__(self, *, parent):
        """
        Scan Manager loads and manages the available scans.
        """
        self.parent = parent
        self.available_scans = {}
        self.scan_dict = {}
        self._plugins = {}
        self.load_plugins()
        self.update_available_scans()
        self.publish_available_scans()

    def load_plugins(self):
        """load scan plugins"""
        plugin_path = os.environ.get("BEC_PLUGIN_PATH")
        if not plugin_path:
            logger.info("BEC_PLUGIN_PATH not set. Using default plugin path.")
            plugin_path = self.DEFAULT_PLUGIN_PATH
        else:
            logger.info(f"Using plugin path {plugin_path}")
        plugin_path = os.path.join(plugin_path, "scan_server/scan_plugins")
        files = glob.glob(os.path.join(plugin_path, "*.py"))
        for file in files:
            if file.endswith("__init__.py"):
                continue
            module_spec = importlib.util.spec_from_file_location("scan_plugins", file)
            plugin_module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(plugin_module)
            module_members = inspect.getmembers(plugin_module)
            for name, cls in module_members:
                if not inspect.isclass(cls):
                    continue
                # ignore imported classes
                if cls.__module__ != "scan_plugins":
                    continue
                if issubclass(cls, ScanServerScans.RequestBase):
                    self._plugins[name] = cls
                    logger.info(f"Loading scan plugin {name}")

    def update_available_scans(self):
        """load all scans and plugin scans"""
        members = inspect.getmembers(ScanServerScans)
        for member_name, cls in self._plugins.items():
            members.append((member_name, cls))

        for name, scan_cls in members:
            try:
                is_scan = issubclass(scan_cls, ScanServerScans.RequestBase)
            except TypeError:
                is_scan = False

            if not is_scan or not scan_cls.scan_name:
                logger.debug(f"Ignoring {name}")
                continue
            if scan_cls.scan_name in self.available_scans:
                logger.error(f"{scan_cls.scan_name} already exists. Skipping.")
                continue
            self.scan_dict[scan_cls.__name__] = scan_cls
            self.available_scans[scan_cls.scan_name] = {
                "class": scan_cls.__name__,
                "arg_input": scan_cls.arg_input,
                "required_kwargs": scan_cls.required_kwargs,
                "arg_bundle_size": scan_cls.arg_bundle_size,
                "scan_report_hint": scan_cls.scan_report_hint,
                "doc": scan_cls.__doc__ or scan_cls.__init__.__doc__,
                "signature": signature_to_dict(scan_cls.__init__),
            }

    def publish_available_scans(self):
        """send all available scans to the broker"""
        self.parent.producer.set(
            MessageEndpoints.available_scans(), msgpack.dumps(self.available_scans)
        )
