from abc import abstractmethod, ABC
from sys import stdout
from typing import Optional

import requests

from exporter.config.config import Option, get_default_config, Config


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
    def stop(self) -> None:
        """
        用来关闭连接，它只会被调用一次因此不用担心幂等性问题，但是可能存在并发调用，需要上层Exporter通过sync.Once来控制。
        """
        pass

    @abstractmethod
    def upload_data(self, data: str) -> None:
        """
        UploadData用来发送任意数据，可能会并发调用。
        """
        pass


class StdoutClient(Client):
    """
    StdoutClient 是 Client 的本地文件发送实现类。
    """

    def __init__(self, path: Optional[str] = None):
        if path is not str or path.strip() == "":
            path = "./AnyRobotData.txt"
        self._path = path
        self._stopped = False

    def path(self) -> str:
        return self._path

    def stop(self) -> None:
        self._stopped = True
        return

    def upload_data(self, data: str) -> None:
        if not self._stopped:
            stdout.write(data)
            stdout.flush()
            with open(self._path, "a") as file:
                file.write(data)
                file.flush()
            file.close()
        return


class HTTPClient(Client):
    """
    HTTPClient 是 Client 的HTTP发送实现类。
    """

    def __init__(self, *options: Option):
        cfg = Config()
        for o in options:
            cfg = o.apply(cfg)
        self._http_config = cfg
        self._retry_config = None
        self._http_client = requests.Session()
        self._stopped = False

    def path(self) -> str:
        return self._http_config.endpoint

    def stop(self) -> None:
        self._stopped = True
        self._http_client.close()
        return

    def upload_data(self, data: str) -> None:
        resp = self._http_client.post(
            url=self._http_config.endpoint,
            data=data.encode(encoding="utf8"),
            headers=self._http_config.headers,
            verify=None,
        )
        match resp.status_code:
            case 200, 204:
                print("success")
            case 400:
                # self._retry_config
                pass

        return
