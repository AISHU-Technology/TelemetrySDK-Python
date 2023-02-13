import unittest

from exporter.ar_metric.metric_exporter import ARMetricExporter
from exporter.public.client import StdoutClient


class TestMetricExporter(unittest.TestCase):
    def test_force_flush(self):
        metric_exporter = ARMetricExporter(StdoutClient())
        self.assertEqual(metric_exporter.force_flush(), True)

    def test_shutdown(self):
        metric_exporter = ARMetricExporter(StdoutClient())
        self.assertIsNone(metric_exporter.shutdown())
