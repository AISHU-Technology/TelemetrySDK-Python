import unittest
from exporter.ar_metric.metric_exporter import ARMetricExporter
from exporter.public.client import StdoutClient

metric_exporter = ARMetricExporter(StdoutClient())


class TestMetricExporter(unittest.TestCase):
    def test_export(self):
        # self.assertEqual(metric_exporter.export("正确的数据"), MetricExportResult.SUCCESS)
        # self.assertEqual(metric_exporter.export("错误的数据"), MetricExportResult.FAILURE)
        pass

    def test_force_flush(self):
        self.assertEqual(metric_exporter.force_flush(), False)

    def test_shutdown(self):
        self.assertIsNone(metric_exporter.shutdown())

    def test_export_metrics(self):
        # self.assertEqual(metric_exporter.export_metrics("正确的数据"), False)
        # self.assertEqual(metric_exporter.export_metrics("错误的数据"), False)
        pass
