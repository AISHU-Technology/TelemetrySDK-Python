from abc import abstractmethod, ABC
from enum import IntEnum
from typing import Iterable


class Compression(IntEnum):
    NoCompression = 0
    GzipCompression = 1


class Config:
    def __init__(self):
        self.endpoint: str = "localhost:5678"
        self.compression: Compression = Compression.GzipCompression
        self.timeout: float = 10
        self.headers: "dict[str, str]" = {}
        self.max_elapsed_time: float = 60
        self.is_sync: bool = False

    def __eq__(self, other) -> bool:
        if not isinstance(other, Config):
            return False
        return self.__dict__ == other.__dict__


class Option(ABC):
    @abstractmethod
    def apply(self, cfg: Config) -> Config:
        pass
