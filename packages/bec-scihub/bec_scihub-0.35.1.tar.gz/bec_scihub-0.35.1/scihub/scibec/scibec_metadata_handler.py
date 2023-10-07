from __future__ import annotations

from typing import TYPE_CHECKING

from bec_lib.core import BECMessage, MessageEndpoints, bec_logger

logger = bec_logger.logger

if TYPE_CHECKING:
    from scihub.scibec import SciBecConnector


class SciBecMetadataHandler:
    def __init__(self, scibec_connector: SciBecConnector) -> None:
        self.scibec_connector = scibec_connector
        self._scan_status_consumer = None
        self._start_scan_subscription()
        self._scan_segment_subscription = None
        self._start_scan_segment_subscription()
        self._baseline_subscription = None
        self._start_baseline_subscription()

    def _start_scan_subscription(self):
        self._scan_status_consumer = self.scibec_connector.connector.consumer(
            MessageEndpoints.scan_status(),
            cb=self._handle_scan_status,
            parent=self,
        )
        self._scan_status_consumer.start()

    def _start_scan_segment_subscription(self):
        self._scan_segment_subscription = self.scibec_connector.connector.consumer(
            MessageEndpoints.scan_segment(),
            cb=self._handle_scan_data,
            parent=self,
        )
        self._scan_segment_subscription.start()

    def _start_baseline_subscription(self):
        self._baseline_subscription = self.scibec_connector.connector.consumer(
            MessageEndpoints.scan_baseline(),
            cb=self._handle_baseline_data,
            parent=self,
        )
        self._baseline_subscription.start()

    @staticmethod
    def _handle_scan_status(msg, *, parent, **_kwargs) -> None:
        msg = BECMessage.ScanStatusMessage.loads(msg.value)
        try:
            scan = parent.update_scan_data(msg)
        except Exception:
            logger.warning("Failed to write to SciBec")
            return

        # if msg.content["status"] != "open":
        #     parent.update_event_data(scan)

    def update_scan_data(self, msg) -> dict:
        scibec = self.scibec_connector.scibec
        scibec_info = self.scibec_connector.scibec_info
        session_id = scibec_info["activeSession"][0]["id"]
        experiment_id = scibec_info["activeSession"][0]["experimentId"]
        logger.debug(f"Received new scan status {msg}")
        scan = scibec.get_scan_by_scanID(msg.content["scanID"])
        if not scan:
            info = msg.content["info"]
            dataset_number = info.get("dataset_number")
            dataset = scibec.get_dataset_by_experiment_and_number(experiment_id, dataset_number)
            if not dataset:
                dataset_data = {"experimentId": experiment_id, "number": dataset_number}
                dataset = scibec.add_dataset(dataset_data)
            if isinstance(dataset, list):
                dataset = dataset[0]
            scan_data = {
                "scanType": info.get("scan_name", ""),
                "scanId": info.get("scanID", ""),
                "queueId": info.get("queueID", ""),
                "requestId": info.get("RID", ""),
                "exitStatus": msg.content["status"],
                "queue": info.get("stream", ""),
                "metadata": info,
                "sessionId": session_id,
                "datasetId": dataset["id"],
                "scanNumber": info.get("scan_number", 0),
            }
            scan = scibec.add_scan(scan_data)
        else:
            info = msg.content["info"]
            update_data = {"metadata": info, "exitStatus": msg.content["status"]}
            scibec.patch_scan(scan[0]["id"], update_data)
        return scan

    @staticmethod
    def _handle_scan_data(msg, *, parent, **_kwargs) -> None:
        msg = BECMessage.ScanMessage.loads(msg.value)

    @staticmethod
    def _handle_baseline_data(msg, *, parent, **_kwargs) -> None:
        msg = BECMessage.ScanBaselineMessage.loads(msg.value)

    def update_event_data(self, scan_info: dict) -> None:
        baseline_data = self.scibec_connector.producer.get(
            MessageEndpoints.public_scan_baseline(scan_info[0]["scanId"])
        )
        baseline_data = BECMessage.ScanBaselineMessage.loads(baseline_data)
