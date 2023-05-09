import typing

from opentelemetry import trace
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from exporter.common.ar_trace import anyrobot_traces_from_trace_spans
from exporter.public.client import Client
from exporter.public.exporter import Exporter
from exporter.version.version import TraceInstrumentationName, TelemetrySDKVersion, TraceInstrumentationURL


class ARTraceExporter(SpanExporter):
    """
    ARTraceExporter 导出数据到AnyRobot Feed Ingester的 Trace 数据接收器。
    """

    def __init__(self, client: Client):
        self._exporter: Exporter = Exporter(client)
        SpanExporter.__init__(self)

    def export(
            self, spans: typing.Sequence[ReadableSpan]
    ) -> "SpanExportResult":
        """
        判断发送成功或失败。
        """
        if self.export_traces(spans):
            return SpanExportResult.FAILURE
        return SpanExportResult.SUCCESS

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        """
        没有缓存，所以不操作。
        """
        return False

    def shutdown(self) -> None:
        """
        关闭实际写数据的 Client。
        """
        self._exporter.client.stop()

    def export_traces(self, traces_data: typing.Sequence[ReadableSpan]) -> bool:
        """
        先转换数据和golang统一。
        """
        data = anyrobot_traces_from_trace_spans(traces_data)
        return self._exporter.client.upload_data(data)


tracer = trace.get_tracer(TraceInstrumentationName, TelemetrySDKVersion, None, TraceInstrumentationURL)
