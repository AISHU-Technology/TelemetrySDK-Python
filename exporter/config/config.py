from abc import abstractmethod, ABC


class Config:
    def __init__(self):
        pass

    endpoint = None
    headers = {}


class Option(ABC):
    @abstractmethod
    def apply(self, cfg: Config) -> Config:
        pass


class URL(Option):
    def __init__(self, url: str):
        self._url = url

    def apply(self, cfg: Config) -> Config:
        cfg.endpoint = self._url
        return cfg


def withurl(url: str) -> Option:
    option = URL(url)
    return option


@staticmethod
def get_default_config() -> Config:
    default_config = Config()
    return default_config
