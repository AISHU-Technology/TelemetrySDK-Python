from opentelemetry.sdk.metrics._internal.export import (
    MetricExporter,
    MetricExportResult,
)
from opentelemetry.sdk.metrics._internal.point import MetricsData
from exporter.common.ar_metric import  anyrobot_metrics_from_resource_metrics
from exporter.public.client import Client, StdoutClient
from exporter.public.exporter import Exporter


class ARMetricExporter(MetricExporter):
    def __init__(self, client: Client):
        self._exporter = Exporter(client)
        MetricExporter.__init__(self)

    def export(
        self,
        metrics_data: MetricsData,
        timeout_millis: float = 10_000,
        **kwargs,
    ) -> MetricExportResult:
        self.export_metrics(metrics_data)
        return MetricExportResult.SUCCESS

    def force_flush(self, timeout_millis: float = 10_000) -> bool:
        return True

    def shutdown(self, timeout_millis: float = 30_000, **kwargs) -> None:
        self._exporter.client().stop()

    def export_metrics(self, metrics_data: MetricsData):
        data = anyrobot_metrics_from_resource_metrics(metrics_data)
        self._exporter.client().upload_data(data)
