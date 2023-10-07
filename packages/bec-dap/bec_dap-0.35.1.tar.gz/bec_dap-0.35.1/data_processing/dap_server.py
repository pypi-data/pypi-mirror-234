from bec_lib.core import BECService
from bec_lib.core.connector import ConnectorBase
from bec_lib.core.service_config import ServiceConfig

from .worker_manager import DAPWorkerManager


class DAPServer(BECService):
    """Data processing server class."""

    def __init__(
        self, config: ServiceConfig, connector_cls: ConnectorBase, unique_service=False
    ) -> None:
        super().__init__(config, connector_cls, unique_service)
        self._work_manager = None
        self._start_manager()

    def _start_manager(self):
        self._work_manager = DAPWorkerManager(self.connector)

    def shutdown(self):
        self._work_manager.shutdown()
        super().shutdown()
