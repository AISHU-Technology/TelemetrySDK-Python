from abc import abstractmethod, ABC
from typing import Dict


class Config:
    def __init__(self):
        self.endpoint = "localhost:5678"
        self.compression = 1
        self.timeout = 100
        self.headers = dict[str, str]
        self.max_elapsed_time = 100


class Option(ABC):
    @abstractmethod
    def apply(self, cfg: Config) -> Config:
        pass
