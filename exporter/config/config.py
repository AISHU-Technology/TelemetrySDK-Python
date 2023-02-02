from abc import abstractmethod, ABC
from enum import IntEnum
from typing import Iterable


class Compression(IntEnum):
    NoCompression = 0
    GzipCompression = 1


class Config:
    def __init__(self, current: int = 0):
        self.current = current
        self.endpoint: str = "localhost:5678"
        self.compression: Compression = Compression.GzipCompression
        self.timeout: float = 10
        self.headers: dict[str, str] = {}
        self.max_elapsed_time: float = 60

    def __iter__(self) -> Iterable:
        return self

    def __next__(self):
        if self.current > 4 or self.current < 0:
            raise StopIteration
        self.current += 1
        return self.__getitem__(self.current)

    def __getitem__(self, item: int):
        match item:
            case 1:
                return self.endpoint
            case 2:
                return self.compression
            case 3:
                return self.timeout
            case 4:
                return self.headers
            case 5:
                return self.max_elapsed_time

    def __eq__(self, other) -> bool:
        if not isinstance(other, Config):
            return False
        for attr in self:
            if attr != other.__getitem__(self.current):
                self.current = 0
                return False
        self.current = 0
        return True


class Option(ABC):
    @abstractmethod
    def apply(self, cfg: Config) -> Config:
        pass
