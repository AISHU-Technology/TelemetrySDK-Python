from exporter.common.ar_log import anyrobot_logs_from_logs
from exporter.public.client import Client
from exporter.public.exporter import Exporter
from tlogging.exporter import LogExporter


class ARLogExporter(LogExporter):
    """
    ARLogExporter 导出数据到AnyRobot Feed Ingester的 Log 数据接收器。
    """

    def __init__(self, client: Client):
        self._exporter: Exporter = Exporter(client)
        LogExporter.__init__(self)

    def name(self) -> str:
        """
        返回client地址。
        """
        return self._exporter.client.path()

    def shutdown(self, timeout_millis: float = 30_000, **kwargs) -> None:
        """
        关闭实际写数据的 Client。
        """
        self._exporter.client.stop()

    def export_logs(self, logs: list["_Span"]) -> bool:
        """
        先转换数据和golang统一。
        """
        data = anyrobot_logs_from_logs(logs)
        return self._exporter.client.upload_data(data)
