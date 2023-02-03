from abc import abstractmethod, ABC
from sys import stdout
from time import sleep
from typing import Optional, Generator, Any
from io import BytesIO
import requests
import gzip
import logging

from exporter.config.config import Option, Config
from exporter.custom_errors.error_code import *
from exporter.public.public import Compression
import backoff

_is_backoff_v2 = next(backoff.expo()) is None
_logger = logging.getLogger(__name__)


class Client(ABC):
    """
    Client 负责连接数据接收器，并且负责转换数据格式并发送可观测性数据，内部为net/http/public。
    """

    @abstractmethod
    def path(self) -> str:
        """
        path 用来获取上报地址。
        """
        pass

    @abstractmethod
    def stop(self) -> bool:
        """
        用来关闭连接，它只会被调用一次因此不用担心幂等性问题，但是可能存在并发调用，需要上层Exporter通过sync.Once来控制。
        """
        pass

    @abstractmethod
    def upload_data(self, data: str) -> bool:
        """
        UploadData用来发送任意数据，可能会并发调用。
        """
        pass


class StdoutClient(Client):
    """
    StdoutClient 是 Client 的本地文件发送实现类。
    """

    def __init__(self, path: Optional[str] = None):
        if not isinstance(path, str) or path.strip() == "":
            path = "./AnyRobotData.txt"
        self._path = path

    def path(self) -> str:
        return self._path

    def stop(self) -> bool:
        return False

    def upload_data(self, data: str) -> bool:
        stdout.write(data)
        stdout.flush()
        with open(self._path, "w") as file:
            file.write(data)
            file.flush()
        return False


class HTTPClient(Client):
    """
    HTTPClient 是 Client 的HTTP发送实现类。
    """

    def __init__(self, *options: Option):
        cfg = Config()
        for o in options:
            cfg = o.apply(cfg)
        self._http_config = cfg
        self._http_client = requests.Session()
        self._exporting_data = None

    def path(self) -> str:
        return self._http_config.endpoint

    def stop(self) -> bool:
        self._http_client.close()
        return False

    @staticmethod
    def _retry(max_elapsed_time: float) -> Generator[float, Any, None]:
        gen = backoff.expo(max_value=max_elapsed_time)
        if _is_backoff_v2:
            gen.send(None)
        return gen

    def upload_data(self, data: str) -> bool:
        """
        实际发送可观测性数据的函数。
        """
        # 设置压缩方式和数据来源
        self._http_config.headers["Service-Language"] = "Python"
        if self._http_config.compression == Compression.NoCompression:
            self._exporting_data = data.encode(encoding="utf8")
            self._http_config.headers["Content-Encoding"] = "json"
        if self._http_config.compression == Compression.GzipCompression:
            gzip_data = BytesIO()
            with gzip.GzipFile(fileobj=gzip_data, mode="w") as gzip_stream:
                gzip_stream.write(bytes(data, "utf8"))
            self._exporting_data = gzip_data.getvalue()
            self._http_config.headers["Content-Encoding"] = "gzip"

        for delay in self._retry(self._http_config.max_elapsed_time):
            if delay == self._http_config.max_elapsed_time:
                return True
            resp = self._http_client.post(
                url=self._http_config.endpoint,
                data=self._exporting_data,
                headers=self._http_config.headers,
                verify=None,
                timeout=self._http_config.timeout,
            )
            if resp.status_code == 200 or 204:
                return False
            if resp.status_code == 400:
                _logger.info(InvalidFormat)
                return True
            if resp.status_code == 404:
                _logger.info(JobIdNotFound)
                return True
            if resp.status_code == 413:
                _logger.info(PayloadTooLarge)
                return True
            if resp.status_code == 429 or 500 or 503:
                self._http_config.headers["Retry-After"] = "true"
                sleep(delay)
                continue
            _logger.info(
                "Failed to export , status code: %s, reason: %s",
                resp.status_code,
                resp.text,
            )
            return True
        return False
