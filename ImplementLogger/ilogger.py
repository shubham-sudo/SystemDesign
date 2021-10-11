from abc import ABC, abstractmethod
from datetime import datetime


class ILogger(ABC):
    @abstractmethod
    def start(self, process_id: str, start_time: datetime):
        ...

    @abstractmethod
    def end(self, process_id: str, end_time: datetime):
        ...

    @abstractmethod
    def poll(self):
        ...
