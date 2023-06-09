import unittest
from opentelemetry.sdk.trace.export import SpanExportResult
from exporter.ar_trace.trace_exporter import ARTraceExporter
from exporter.public.client import StdoutClient

trace_exporter = ARTraceExporter(StdoutClient())


class TestTraceExporter(unittest.TestCase):
    def test_export(self):
        # self.assertEqual(trace_exporter.export("正确的数据"), SpanExportResult.SUCCESS)
        # self.assertEqual(trace_exporter.export("错误的数据"), SpanExportResult.FAILURE)
        pass

    def test_force_flush(self):
        self.assertEqual(trace_exporter.force_flush(), False)

    def test_shutdown(self):
        self.assertIsNone(trace_exporter.shutdown())

    def test_export_traces(self):
        # self.assertEqual(metric_exporter.export_metrics("正确的数据"), False)
        # self.assertEqual(metric_exporter.export_metrics("错误的数据"), False)
        pass


if __name__ == "__main__":
    unittest.main()
