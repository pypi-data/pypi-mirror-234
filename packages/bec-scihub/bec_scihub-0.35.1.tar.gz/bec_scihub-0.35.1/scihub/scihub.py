from bec_lib.core import BECService, ServiceConfig
from bec_lib.core.connector import ConnectorBase

from scihub.scibec import SciBecConnector
from scihub.scilog import SciLogConnector


class SciHub(BECService):
    def __init__(self, config: ServiceConfig, connector_cls: ConnectorBase) -> None:
        super().__init__(config, connector_cls, unique_service=True)
        self.config = config
        self.scibec_connector = None
        self.scilog_connector = None
        self._start_scibec_connector()
        self._start_scilog_connector()

    def _start_scibec_connector(self):
        self.scibec_connector = SciBecConnector(self, self.connector)

    def _start_scilog_connector(self):
        self.scilog_connector = SciLogConnector(self, self.connector)

    def shutdown(self):
        super().shutdown()
        self.scibec_connector.shutdown()
        self.scilog_connector.shutdown()
