import re
from enum import IntEnum
from typing import Union

from exporter.config.config import Option, Config
from exporter.custom_errors.error_code import *


class WithAnyRobotURL(Option):
    def __init__(self, url: str):
        if not re.match(r"^https?:/{2}\w.+$", url):
            raise Exception(InvalidURL)
        self._url = url

    def apply(self, cfg: Config) -> Config:
        cfg.endpoint = self._url
        return cfg


class Compression(IntEnum):
    NoCompression = 0
    GzipCompression = 1


class WithCompression(Option):
    def __init__(self, compression: Compression):
        if compression < 0 or compression > 1:
            raise Exception(InvalidCompression)
        self._compression = compression

    def apply(self, cfg: Config) -> Config:
        cfg.compression = self._compression
        return cfg


class WithTimeout(Option):
    """
    ???
    """

    def __init__(self, compression: Union[int, Compression]):
        if len(compression) < 0:
            raise Exception("sd")
        self._compression = compression

    def apply(self, cfg: Config) -> Config:
        cfg.compression = self._compression
        return cfg


class WithHeader(Option):
    def __init__(self, headers: dict[str, str]):
        self._headers = headers

    def apply(self, cfg: Config) -> Config:
        cfg.headers = self._headers
        return cfg


class WithRetry(Option):
    """
    ???
    """

    def __init__(self, compression: Union[int, Compression]):
        if len(compression) < 0:
            raise Exception("sd")
        self._compression = compression

    def apply(self, cfg: Config) -> Config:
        cfg.compression = self._compression
        return cfg
