from __future__ import annotations

import time
import uuid
from collections.abc import Iterable
from typing import TYPE_CHECKING

import msgpack
import numpy as np

from bec_lib.core import MessageEndpoints, bec_logger

from .emitter import EmitterBase

logger = bec_logger.logger

if TYPE_CHECKING:
    from .scan_bundler import ScanBundler


class BlueskyEmitter(EmitterBase):
    def __init__(self, scan_bundler: ScanBundler) -> None:
        super().__init__(scan_bundler.producer)
        self.scan_bundler = scan_bundler
        self.bluesky_metadata = {}

    def send_run_start_document(self, scanID) -> None:
        """Bluesky only: send run start documents."""
        logger.debug(f"sending run start doc for scanID {scanID}")
        self.bluesky_metadata[scanID] = {}
        doc = self._get_run_start_document(scanID)
        self.bluesky_metadata[scanID]["start"] = doc
        self.producer.send(MessageEndpoints.bluesky_events(), msgpack.dumps(("start", doc)))
        self.send_descriptor_document(scanID)

    def _get_run_start_document(self, scanID) -> dict:
        sb = self.scan_bundler
        doc = {
            "time": time.time(),
            "uid": str(uuid.uuid4()),
            "scanID": scanID,
            "queueID": sb.sync_storage[scanID]["info"]["queueID"],
            "scan_id": sb.sync_storage[scanID]["info"]["scan_number"],
            "motors": tuple(dev.name for dev in sb.scan_motors[scanID]),
        }
        return doc

    def _get_data_keys(self, scanID):
        sb = self.scan_bundler
        signals = {}
        for dev in sb.monitored_devices[scanID]["devices"]:
            # copied from bluesky/callbacks/stream.py:
            for key, val in dev.signals.items():
                val = val["value"]
                # String key
                if isinstance(val, str):
                    key_desc = {"dtype": "string", "shape": []}
                # Iterable
                elif isinstance(val, Iterable):
                    key_desc = {"dtype": "array", "shape": np.shape(val)}
                # Number
                else:
                    key_desc = {"dtype": "number", "shape": []}
                signals[key] = key_desc
        return signals

    def _get_descriptor_document(self, scanID) -> dict:
        sb = self.scan_bundler
        doc = {
            "run_start": self.bluesky_metadata[scanID]["start"]["uid"],
            "time": time.time(),
            "data_keys": self._get_data_keys(scanID),
            "uid": str(uuid.uuid4()),
            "configuration": {},
            "name": "primary",
            "hints": {
                "samx": {"fields": ["samx"]},
                "samy": {"fields": ["samy"]},
            },
            "object_keys": {
                dev.name: list(dev.signals.keys())
                for dev in sb.monitored_devices[scanID]["devices"]
            },
        }
        return doc

    def send_descriptor_document(self, scanID) -> None:
        """Bluesky only: send descriptor document"""
        doc = self._get_descriptor_document(scanID)
        self.bluesky_metadata[scanID]["descriptor"] = doc
        self.producer.send(MessageEndpoints.bluesky_events(), msgpack.dumps(("descriptor", doc)))

    def cleanup_storage(self, scanID):
        """remove old scanIDs to free memory"""

        for storage in [
            "bluesky_metadata",
        ]:
            try:
                getattr(self, storage).pop(scanID)
            except KeyError:
                logger.warning(f"Failed to remove {scanID} from {storage}.")

    def send_bluesky_scan_point(self, scanID, pointID) -> None:
        self.producer.send(
            MessageEndpoints.bluesky_events(),
            msgpack.dumps(("event", self._prepare_bluesky_event_data(scanID, pointID))),
        )

    def _prepare_bluesky_event_data(self, scanID, pointID) -> dict:
        # event = {
        #     "descriptor": "5605e810-bb4e-4e40-b...d45279e3a4",
        #     "time": 1648468217.524021,
        #     "data": {
        #         "det": 1.0,
        #         "motor1": -10.0,
        #         "motor1_setpoint": -10.0,
        #         "motor2": -10.0,
        #         "motor2_setpoint": -10.0,
        #     },
        #     "timestamps": {
        #         "det": 1648468209.868633,
        #         "motor1": 1648468209.862141,
        #         "motor1_setpoint": 1648468209.8607192,
        #         "motor2": 1648468209.864479,
        #         "motor2_setpoint": 1648468209.8629901,
        #     },
        #     "seq_num": 1,
        #     "uid": "ea83a56e-6af2-4b94-9...44dcc36d4e",
        #     "filled": {},
        # }
        sb = self.scan_bundler
        metadata = self.bluesky_metadata[scanID]
        while not metadata.get("descriptor"):
            time.sleep(0.01)

        bls_event = {
            "descriptor": metadata["descriptor"].get("uid"),
            "time": time.time(),
            "seq_num": pointID,
            "uid": str(uuid.uuid4()),
            "filled": {},
            "data": {},
            "timestamps": {},
        }
        for data_point in sb.sync_storage[scanID][pointID].values():
            for key, val in data_point.items():
                bls_event["data"][key] = val["value"]
                bls_event["timestamps"][key] = val["timestamp"]
        return bls_event

    def on_cleanup(self, scanID: str):
        self.cleanup_storage(scanID)

    def on_init(self, scanID: str):
        self.send_run_start_document(scanID)
