from __future__ import annotations

import time
from abc import ABC, abstractmethod
from collections import deque
from typing import Any, List, Optional, Tuple

import lmfit
import numpy as np
from bec_lib.core import BECMessage, MessageEndpoints
from bec_lib.core.redis_connector import MessageObject, RedisConnector


def nested_get(data: str, keys, default=None):
    """
    Get a value from a nested dictionary.

    Args:
        data (dict): Dictionary to get the value from.
        keys (str): Keys to get the value from. Keys are separated by a dot.
        default (Any, optional): Default value to return if the key is not found. Defaults to None.

    Returns:
        Any: Value of the key.

    Examples:
        >>> data = {"a": {"b": 1}}
        >>> nested_get(data, "a.b")
        1
    """
    if "." in keys:
        key, rest = keys.split(".", 1)
        return nested_get(data[key], rest, default=default)
    return data.get(keys, default)


class StreamProcessor(ABC):
    """
    Abstract class for stream processors. This class is responsible for
    processing stream data. Each processor is started in a separate process.
    Override the process method to implement the processing logic.

    Please note that the processor stores the data in the self.data attribute.
    This is done to allow the processor to access multiple data points at once,
    e.g. for fitting.Make sure to reset the data attribute after processing
    the data to avoid memory leaks.
    """

    def __init__(self, connector: RedisConnector, config: dict) -> None:
        """
        Initialize the StreamProcessor class.

        Args:
            connector (RedisConnector): Redis connector.
            config (dict): Configuration for the processor.
        """
        super().__init__()
        self._connector = connector
        self.producer = connector.producer()
        self._process = None
        self.queue = deque()
        self.consumer = None
        self.config = config
        self.data = None

    def reset_data(self):
        """Reset the data."""
        self.data = None

    @abstractmethod
    def process(self, data: dict, metadata: dict) -> Tuple[dict, dict]:
        """
        Process data and return the result.

        Args:
            data (dict): Data to be processed.
            metadata (dict): Metadata associated with the data.

        Returns:
            Tuple[dict, dict]: Tuple containing the processed data and metadata.
        """

    @property
    def status(self):
        """Return the worker status."""
        return {
            "process": self._process,
            "config": self.config,
            "started": self._process.is_alive(),
        }

    def shutdown(self):
        """Shutdown the worker. Terminate the process and wait for it to join."""
        self._process.terminate()
        self._process.join()

    def _run_forever(self):
        """Core method for the worker. This method is called in a while True loop."""
        if not self.queue:
            time.sleep(0.1)
            return
        data = self.queue.popleft()

        # Process data
        result = self._process_data(data)

        # publish the result
        if not all(result):
            return

        # for multiple results, publish them as a bundle
        if isinstance(result, list) and len(result) > 1:
            msg_bundle = BECMessage.BundleMessage()
            for data, metadata in result:
                msg = BECMessage.ProcessedDataMessage(data=data, metadata=metadata).dumps()
                msg_bundle.append(msg)
            self._publish_result(msg_bundle.dumps())
        else:
            msg = BECMessage.ProcessedDataMessage(data=result[0][0], metadata=result[0][1]).dumps()
            self._publish_result(msg)

    def start(self):
        """Run the worker. This method is called in a separate process."""
        while True:
            self._run_forever()

    def _process_data(self, data: BECMessage.BECMessage) -> List[Tuple[dict, dict]]:
        """Process data."""
        if not isinstance(data, list):
            data = [data]

        return [self.process(sub_data.content, sub_data.metadata) for sub_data in data]

    def start_data_consumer(self):
        """Get data from redis."""
        if self.consumer and self.consumer.is_alive():
            self.consumer.shutdown()
        self.consumer = self._connector.consumer(
            self.config["stream"], cb=self._set_data, parent=self
        )
        self.consumer.start()

    @staticmethod
    def _set_data(msg: MessageObject, parent: StreamProcessor):
        """Set data to the parent."""
        parent.queue.append(BECMessage.MessageReader.loads(msg.value))

    def _publish_result(self, msg: BECMessage.BECMessage):
        """Publish the result."""
        self.producer.set_and_publish(
            MessageEndpoints.processed_data(self.config["output"]),
            msg,
        )

    @classmethod
    def run(cls, config: dict, connector_host: list[str]) -> None:
        """Run the worker."""
        connector = RedisConnector(connector_host)

        worker = cls(connector, config)
        worker.start_data_consumer()
        worker.start()


class LmfitProcessor(StreamProcessor):
    """Lmfit processor class."""

    def __init__(self, connector: RedisConnector, config: dict) -> None:
        """
        Initialize the LmfitProcessor class.

        Args:
            connector (RedisConnector): Redis connector.
            config (dict): Configuration for the processor.
        """
        super().__init__(connector, config)
        self.model = self._get_model()
        self.scan_id = None

    def _get_model(self) -> lmfit.Model:
        """Get the model from the config and convert it to an lmfit model."""

        if not self.config:
            raise ValueError("No config provided")
        if not self.config.get("model"):
            raise ValueError("No model provided")

        model = self.config["model"]
        if not isinstance(model, str):
            raise ValueError("Model must be a string")

        # check if the model is a valid lmfit model
        if not hasattr(lmfit.models, model):
            raise ValueError(f"Invalid model: {model}")

        model = getattr(lmfit.models, model)

        return model()

    def process(self, data: dict, metadata: dict) -> Optional[Tuple[dict, dict]]:
        """
        Process data and return the result.

        Args:
            data (dict): Data to be processed.
            metadata (dict): Metadata associated with the data.

        Returns:
            Tuple[dict, dict]: Tuple containing the processed data and metadata. Returns None if no data is provided or if the fit is skipped.
        """

        if not data:
            return None

        # get the event data
        x = nested_get(data.get("data", {}), self.config["input_xy"][0])
        y = nested_get(data.get("data", {}), self.config["input_xy"][1])

        # check if the data is indeed a number
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            return None

        # reset the data if the scan id changed
        if self.scan_id != data.get("scanID"):
            self.reset_data()
            self.scan_id = data.get("scanID")

        # append the data to the data attribute
        if self.data is None:
            self.data = {"x": [], "y": []}
        self.data["x"].append(x)
        self.data["y"].append(y)

        # check if the data is long enough to fit
        if len(self.data["x"]) < 3:
            return None

        # fit the data
        result = self.model.fit(self.data["y"], x=self.data["x"])

        # add the fit result to the output
        stream_output = {
            self.config["output"]: {"x": np.asarray(self.data["x"]), "y": result.best_fit},
            "input": self.config["input_xy"],
        }

        # add the fit parameters to the metadata
        metadata["fit_parameters"] = result.best_values
        metadata["fit_summary"] = result.summary()

        return (stream_output, metadata)
