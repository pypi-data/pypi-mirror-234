from abc import ABC, abstractmethod


class ITelemetryService(ABC):

    @abstractmethod
    def library_loaded(self) -> None:
        pass

    @abstractmethod
    def send_telemetry(self, event: str, info: dict = None) -> None:
        pass
