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

    @property
    def name(self) -> str:
        return self._name

    def shutdown(self) -> bool:
        if self._stopped:
            return False
        self._stopped = True
        return self.client.stop()

    def export_data(self, data: str) -> bool:
        if not self._stopped and len(data) != 0:
            return self.client.upload_data(data)
        return False

    @property
    def client(self) -> Client:
        return self._client
