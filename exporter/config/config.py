from abc import abstractmethod, ABC
from enum import IntEnum


class Compression(IntEnum):
    NoCompression = 0
    GzipCompression = 1


class Config:
    def __init__(self):
        self.endpoint: str = "localhost:5678"
        self.compression: Compression = Compression.GzipCompression
        self.timeout: float = 10
        self.headers: dict[str, str] = {}
        self.max_elapsed_time: float = 60


class Option(ABC):
    @abstractmethod
    def apply(self, cfg: Config) -> Config:
        pass
