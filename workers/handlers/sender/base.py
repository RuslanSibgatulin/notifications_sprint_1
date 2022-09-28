from abc import ABC, abstractmethod


class EmailSenderInterface(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def send(
            self,
            send_from: str,
            send_to: str,
            message: str,
            template: str
    ) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass
