import re
from enum import IntEnum
from typing import Union

from exporter.config.config import Option, Config, Compression
from exporter.custom_errors.error_code import *


class WithAnyRobotURL(Option):
    """
    设置上报地址。
    要求合法的URL格式示例：http://a.b.c.d:0000/address。
    """

    def __init__(self, url: str):
        if not re.match(r"^https?:/{2}\w.+$", url):
            raise Exception(InvalidURL)
        self._url = url

    def apply(self, cfg: Config) -> Config:
        cfg.endpoint = self._url
        return cfg


class WithCompression(Option):
    """
    设置数据压缩方式。
    0代表无压缩，1代表Gzip压缩。
    """

    def __init__(self, compression: Compression):
        if compression < 0 or compression > 1:
            raise Exception(InvalidCompression)
        self._compression = compression

    def apply(self, cfg: Config) -> Config:
        cfg.compression = self._compression
        return cfg


class WithTimeout(Option):
    """
    设置HTTP连接超时时间，单位秒。
    """

    def __init__(self, timeout: int):
        if timeout <= 0 or timeout > 120:
            raise Exception(DurationTooLong)
        self._timeout = timeout

    def apply(self, cfg: Config) -> Config:
        cfg.timeout = self._timeout
        return cfg


class WithHeader(Option):
    """
    设置自定义请求头。
    """

    def __init__(self, headers: dict[str, str]):
        self._headers = headers

    def apply(self, cfg: Config) -> Config:
        cfg.headers = self._headers
        return cfg


class WithRetry(Option):
    """
    设置重发规则，最长重发时间，单位秒。
    """

    def __init__(self, max_elapsed_time: float):
        if max_elapsed_time <= 0 or max_elapsed_time > 600:
            raise Exception(RetryTooLong)
        self._max_elapsed_time = max_elapsed_time

    def apply(self, cfg: Config) -> Config:
        cfg.max_elapsed_time = self._max_elapsed_time
        return cfg
