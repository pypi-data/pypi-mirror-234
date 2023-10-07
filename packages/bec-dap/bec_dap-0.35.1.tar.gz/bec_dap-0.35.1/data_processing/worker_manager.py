from __future__ import annotations

import inspect
import multiprocessing as mp
from typing import Any, List

from bec_lib.core import BECMessage, MessageEndpoints, bec_logger
from bec_lib.core.redis_connector import RedisConnector

from .stream_processor import LmfitProcessor

logger = bec_logger.logger

try:
    import bec_plugins.data_processing as dap_plugins
except ImportError:
    dap_plugins = None
    logger.info("Failed to import bec_plugins.data_processing")


class DAPWorkerManager:
    """Data processing worker manager class."""

    def __init__(self, connector: RedisConnector):
        self.connector = connector
        self.producer = connector.producer()
        self._workers = {}
        self._config = {}
        self._worker_plugins = {}
        self._update_available_plugins()
        self._update_config()
        self._start_config_consumer()

    def _update_available_plugins(self):
        """Update the available plugins."""
        self._worker_plugins["LmfitProcessor"] = LmfitProcessor

        if not dap_plugins:
            return
        members = inspect.getmembers(dap_plugins)
        for name, cls in members:
            if not inspect.isclass(cls):
                continue
            if not hasattr(cls, "run") or not callable(cls.run):
                continue
            self._worker_plugins[name] = cls
            logger.info(f"Loading dap plugin {name}")

    #     self._publish_available_plugins()

    # def _publish_available_plugins(self):
    #     """Publish the available plugins."""
    #     logger.debug("Publishing available plugins")

    #     # }
    #     # msg = BECMessage.AvailableResourceMessage(resource={})
    #     self.producer.publish(MessageEndpoints.dap_available_plugins(), msg.dumps())

    def _update_config(self):
        """Get config from redis."""
        logger.debug("Getting config from redis")
        msg = self.producer.get(MessageEndpoints.dap_config())
        if not msg:
            return
        config_msg = BECMessage.DAPConfigMessage.loads(msg)
        if not config_msg:
            return
        self.update_config(config_msg)

    def _start_config_consumer(self):
        """Get config from redis."""
        logger.debug("Starting config consumer")
        self.consumer = self.connector.consumer(
            MessageEndpoints.dap_config(), cb=self._set_config, parent=self
        )
        self.consumer.start()

    @staticmethod
    def _set_config(msg: BECMessage.BECMessage, parent: DAPWorkerManager) -> None:
        """Set config to the parent."""
        msg = BECMessage.DAPConfigMessage.loads(msg.value)
        if not msg:
            return
        parent.update_config(msg)

    def update_config(self, msg: BECMessage.DAPConfigMessage):
        """Update the config."""
        logger.debug(f"Updating config: {msg.content}")
        if not msg.content["config"]:
            return
        self._config = msg.content["config"]

        for worker_config in self._config["workers"]:
            worker_cls = worker_config.get("config", {}).get("worker_cls")
            if not worker_cls:
                logger.error(f"Worker class not found in config: {self._config}")
                continue
            if worker_cls not in self._worker_plugins:
                logger.error(f"Worker class not found: {worker_cls}")
                continue
            # Check if the worker is already running and start it if not
            if worker_config["id"] not in self._workers:
                self._start_worker(worker_config, self._worker_plugins[worker_cls])
                continue

            # Check if the config has changed
            if self._workers[worker_config["id"]]["config"] == worker_config["config"]:
                logger.debug(f"Worker config has not changed: {worker_config['id']}")
                continue

            # If the config has changed, terminate the worker and start a new one
            logger.debug(f"Restarting worker: {worker_config['id']}")
            self._workers[worker_config["id"]]["worker"].terminate()
            self._start_worker(worker_config, self._worker_plugins[worker_cls])

        # Check if any workers need to be removed
        for worker_id in list(self._workers):
            if worker_id not in [worker["id"] for worker in self._config["workers"]]:
                logger.debug(f"Removing worker: {worker_id}")
                self._workers[worker_id]["worker"].terminate()
                del self._workers[worker_id]

    def _start_worker(self, config: dict, worker_cls: Any) -> None:
        """
        Start a worker.

        Args:
            config (dict): Worker config
            worker_cls (Any): Worker class
        """
        logger.debug(f"Starting worker: {config}")

        self._workers[config["id"]] = {
            "worker": self.run_worker(
                config["config"], worker_cls=worker_cls, connector_host=self.connector.bootstrap
            ),
            "config": config["config"],
        }

    def shutdown(self):
        for worker in self._workers.values():
            worker["worker"].terminate()

    @staticmethod
    def run_worker(config: dict, worker_cls: Any, connector_host: List[str]) -> mp.Process:
        """Run the worker."""
        worker = mp.Process(
            target=worker_cls.run,
            kwargs={"config": config, "connector_host": connector_host},
            daemon=True,
        )
        worker.start()
        return worker
