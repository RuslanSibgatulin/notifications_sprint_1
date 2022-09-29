from abc import abstractmethod
from typing import Protocol


class BaseQueueBackend(Protocol):
    @abstractmethod
    def publish(self, routing_key: str, message: bytes) -> None:
        raise NotImplementedError
