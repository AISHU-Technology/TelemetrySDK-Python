from exporter.public.client import Client


class Exporter:
    """
    Exporter: 导出可观测性数据到 AnyRobot Feed Ingester 的数据接收器。
    name: Exporter身份证，同名视为同一个发送器，本质为上报地址。
    shutdown: 关闭Exporter，关闭HTTP连接，丢弃导出缓存。
    export_data: 批量发送可观测性数据到 AnyRobot Feed Ingester 的数据接收器。
    """

    def __init__(self, client: Client):
        self._name = client.path()
        self._client = client
        self._stopped = False

    def name(self) -> str:
        return self._name

    def shutdown(self) -> None:
        self._stopped = True
        self.client().stop()
        return

    def export_data(self, data: str) -> None:
        if not self._stopped and len(data) != 0:
            self.client().upload_data(data)
        return

    def client(self) -> Client:
        return self._client
