from abc import abstractmethod, ABC


class Config:
    def __init__(self):
        self.insecure = True
        self.endpoint = "localhost:5678"
        self.compression = 0
        self.timeout = 10
        self.headers = {}
        self.tls = {}


@staticmethod
def get_default_config() -> Config:
    return Config()


class Option(ABC):
    @abstractmethod
    def apply(self, cfg: Config) -> Config:
        pass
