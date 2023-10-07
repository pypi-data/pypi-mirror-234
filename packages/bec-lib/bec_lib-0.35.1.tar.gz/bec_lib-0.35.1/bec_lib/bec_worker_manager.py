from __future__ import annotations

from bec_lib.core import BECMessage, MessageEndpoints, RedisConnector


class BECWorker:
    """Helper class for remote BEC workers."""

    def __init__(
        self, id: str, config: dict = None, worker_manager: BECWorkerManager = None
    ) -> None:
        """

        Args:
            config (dict): Configuration dictionary for the worker.
        """
        self.id = id
        self._config = config
        self._worker_manager = worker_manager

    @property
    def config(self) -> dict:
        """Configuration dictionary for the worker."""
        return self._config

    def to_dict(self) -> dict:
        """Converts the BECWorker object to a dictionary."""
        return {"id": self.id, "config": self.config}

    @classmethod
    def from_dict(cls, worker_config: dict, worker_manager: BECWorkerManager) -> BECWorker:
        """Creates a BECWorker object from a dictionary."""
        return cls(**worker_config, worker_manager=worker_manager)

    def update_config(self, config: dict) -> None:
        """Updates the configuration of the worker.

        Args:
            config (dict): Configuration dictionary for the worker.
        """
        self.config.update(config)

    def __eq__(self, other: BECWorker) -> bool:
        """Checks if two BECWorker objects are equal."""
        return self.id == other.id and self.config == other.config

    def __repr__(self) -> str:
        return f"BECWorker(id={self.id}, config={self.config})"


class BECWorkerManager:
    """Class to manage BEC workers used for stream-based data anlysis."""

    def __init__(self, connector: RedisConnector) -> None:
        """

        Args:
            connector (RedisConnector): RedisConnector object to connect to the BEC Redis server.
        """
        self.connector = connector
        self.producer = connector.producer()
        self._workers = []
        self._get_workers()

    def _get_workers(self) -> None:
        """Gets the workers from redis."""
        msg_raw = self.producer.get(MessageEndpoints.dap_config())
        if msg_raw is None:
            return
        msg = BECMessage.DAPConfigMessage.loads(msg_raw)
        self._workers = [
            BECWorker.from_dict(w, self) for w in msg.content["config"].get("workers", [])
        ]

    @property
    def config(self) -> dict:
        """Configuration dictionary for the manager."""
        msg_raw = self.producer.get(MessageEndpoints.dap_config())
        if msg_raw is None:
            return {}
        msg = BECMessage.DAPConfigMessage.loads(msg_raw)
        return msg.content["config"]

    def get_worker(self, id: str) -> BECWorker:
        """Gets a worker from the manager by its id.

        Args:
            id (str): ID of the worker.

        Returns:
            BECWorker: BECWorker object.
        """
        worker = [w for w in self._workers if w.id == id]
        if len(worker) == 0:
            raise ValueError(f"Worker with id {id} does not exist.")
        return worker[0]

    @property
    def workers(self) -> list:
        """List of workers in the manager."""
        worker_config = self.config.get("workers", [])
        return [BECWorker.from_dict(w, self) for w in worker_config]

    @property
    def num_workers(self) -> int:
        """Number of workers in the manager."""
        return len(self.workers)

    def add_worker(self, id: str, config: dict) -> None:
        """Adds a worker to the manager.

        Args:
            id (str): ID of the worker.
            config (dict): Configuration dictionary for the worker.
        """

        # if the worker already exists, raise an error
        if id in [w.id for w in self._workers]:
            raise ValueError(f"Worker with id {id} already exists.")
        self._workers.append(BECWorker(id, config, self))
        self._update_config()

    def update_worker(self, id: str, config: dict) -> None:
        """Updates the configuration of a worker.

        Args:
            id (str): ID of the worker.
            config (dict): Configuration dictionary for the worker.
        """
        worker = self.get_worker(id)
        worker.update_config(config)
        self._update_config()

    def remove_worker(self, id: str) -> None:
        """Removes a worker from the manager.

        Args:
            id (str): ID of the worker.
        """
        self._workers = [w for w in self._workers if w.id != id]
        self._update_config()

    def _update_config(self) -> None:
        """Updates the configuration of the manager."""
        msg = BECMessage.DAPConfigMessage(config={"workers": [w.to_dict() for w in self._workers]})
        self.producer.set_and_publish(MessageEndpoints.dap_config(), msg.dumps())


if __name__ == "__main__":  # pragma: no cover
    from bec_lib.core.redis_connector import RedisConnector

    connector = RedisConnector(["localhost:6379"])
    manager = BECWorkerManager(connector)
    manager.remove_worker("px_dap_worker")
    config = {
        "worker_cls": "SaxsImagingProcessor",
        "output": "px_dap_worker",
    }
    # config = {
    #     "worker_cls": "LmfitProcessor",
    #     "stream": MessageEndpoints.scan_segment(),
    #     "output": "gaussian_fit_worker_3",
    #     "input_xy": ["samx.samx.value", "gauss_bpm.gauss_bpm.value"],
    #     "model": "GaussianModel",
    # }
    manager.add_worker("px_dap_worker", config)
