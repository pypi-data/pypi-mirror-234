from __future__ import annotations

from typing import TYPE_CHECKING

import msgpack
from bec_lib.core import BECMessage, MessageEndpoints, ServiceConfig, bec_logger
from bec_lib.core.connector import ConnectorBase
from requests import ConnectionError

from .config_handler import ConfigHandler
from .scibec import SciBec, SciBecError
from .scibec_metadata_handler import SciBecMetadataHandler

if TYPE_CHECKING:
    from scihub import SciHub

logger = bec_logger.logger


class SciBecConnector:
    def __init__(self, scihub: SciHub, connector: ConnectorBase) -> None:
        self.scihub = scihub
        self.connector = connector
        self.producer = connector.producer()
        self.scibec = None
        self.scibec_info = {}
        self.connect_to_scibec()
        self.update_session()
        self.config_handler = ConfigHandler(self, connector)

        self._config_request_handler = None
        self._metadata_handler = None
        self._start_config_request_handler()
        self._start_metadata_handler()

    @property
    def config(self):
        """get the current service config"""
        return self.scihub.config

    def get_current_session(self):
        if not self.scibec or not self.scibec_info.get("beamline"):
            return None
        if not self.scibec_info["beamline"]["activeExperiment"]:
            return None
        experiment = self.scibec.get_experiment_by_id(
            self.scibec_info["beamline"]["activeExperiment"]
        )
        if not experiment:
            return None
        session_id = experiment[0].get("activeSession")
        if not session_id:
            return None
        self.scibec_info["activeSession"] = self.scibec.get_session_by_id(
            session_id, include_devices=True
        )
        return self.scibec_info["activeSession"]

    def update_session(self):
        session = self.get_current_session()
        if session:
            self.set_redis_config(session[0]["devices"])

    def set_redis_config(self, config):
        self.producer.set(MessageEndpoints.device_config(), msgpack.dumps(config))

    def _start_metadata_handler(self) -> None:
        self._metadata_handler = SciBecMetadataHandler(self)

    def _start_config_request_handler(self) -> None:
        self._config_request_handler = self.connector.consumer(
            MessageEndpoints.device_config_request(),
            cb=self._device_config_request_callback,
            parent=self,
        )
        self._config_request_handler.start()

    @staticmethod
    def _device_config_request_callback(msg, *, parent, **_kwargs) -> None:
        msg = BECMessage.DeviceConfigMessage.loads(msg.value)
        logger.info(f"Received request: {msg}")
        parent.config_handler.parse_config_request(msg)

    def connect_to_scibec(self):
        scibec_host = self.scihub.config.scibec
        if not self.scihub.config.scibec:
            return
        try:
            beamline = self.scihub.config.config["scibec"].get("beamline")
            if not beamline:
                logger.warning(f"Cannot connect to SciBec without a beamline specified.")
                return
            logger.info(f"Connecting to SciBec on {scibec_host}")
            self.scibec = SciBec()
            self.scibec.url = scibec_host
            beamline_info = self.scibec.get_beamline(beamline)
            self.scibec_info["beamline"] = beamline_info
            experiment_id = beamline_info.get("activeExperiment")
            if experiment_id:
                experiment = self.scibec.get_experiment_by_id(experiment_id)
                write_account = experiment[0]["writeAccount"]
                if write_account[0] == "p":
                    write_account = write_account.replace("p", "e")
                self.producer.set(MessageEndpoints.account(), write_account.encode())

                self.scibec_info["activeExperiment"] = experiment
                if not "activeSession" in experiment[0]:
                    return
                session = self.scibec.get_session_by_id(experiment[0]["activeSession"])
                self.scibec_info["activeSession"] = session
            if not beamline_info:
                logger.warning(f"Could not find a beamline with the name {beamline}")
                return
        except (ConnectionError, SciBecError) as exc:
            self.scibec = None
            return

    def shutdown(self):
        pass
