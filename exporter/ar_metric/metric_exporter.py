from opentelemetry.sdk.metrics.export import (
    MetricExporter,
    MetricExportResult,
)
from opentelemetry.sdk.metrics.export import MetricsData
from exporter.common.ar_metric import anyrobot_metrics_from_resource_metrics
from exporter.public.client import Client
from exporter.public.exporter import Exporter
from opentelemetry import metrics
from exporter.version.version import MetricInstrumentationName, TelemetrySDKVersion, MetricInstrumentationURL


class ARMetricExporter(MetricExporter):
    """
    ARMetricExporter 导出数据到AnyRobot Feed Ingester的 Metric 数据接收器。
    """

    def __init__(self, client: Client):
        self._exporter: Exporter = Exporter(client)
        MetricExporter.__init__(self)

    def export(
            self,
            metrics_data: MetricsData,
            timeout_millis: float = 10_000,
            **kwargs,
    ) -> MetricExportResult:
        """
        判断发送成功或失败。
        """
        if self.export_metrics(metrics_data):
            return MetricExportResult.FAILURE
        return MetricExportResult.SUCCESS

    def force_flush(self, timeout_millis: float = 10_000) -> bool:
        """
        没有缓存，所以不操作。
        """
        return False

    def shutdown(self, timeout_millis: float = 30_000, **kwargs) -> None:
        """
        关闭实际写数据的 Client。
        """
        self._exporter.client.stop()

    def export_metrics(self, metrics_data: MetricsData) -> bool:
        """
        先转换数据和golang统一。
        """
        data = anyrobot_metrics_from_resource_metrics(metrics_data)
        return self._exporter.client.upload_data(data)


"""
全局变量，公用一个meter生产Metric数据。
"""
meter = metrics.get_meter_provider().get_meter(
    MetricInstrumentationName, TelemetrySDKVersion, MetricInstrumentationURL
)
