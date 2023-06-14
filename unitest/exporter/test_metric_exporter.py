import unittest

from opentelemetry.sdk.metrics._internal.export import MetricExportResult
from opentelemetry.sdk.metrics._internal.point import MetricsData, ResourceMetrics, ScopeMetrics, Metric, Sum, \
    NumberDataPoint, Histogram, Gauge, HistogramDataPoint
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.util.instrumentation import InstrumentationScope

from exporter.ar_metric.metric_exporter import ARMetricExporter
from exporter.public.client import StdoutClient

metric_exporter = ARMetricExporter(StdoutClient())
test_metric_1 = MetricsData([ResourceMetrics(Resource({"name": "test"}),
                                             [ScopeMetrics(InstrumentationScope(""),
                                                           [Metric("", "", "",
                                                                   Sum([NumberDataPoint({}, 0, 0, 2),
                                                                        NumberDataPoint({}, 0, 0, 2.0)], 0, False))],
                                                           "")],
                                             "")])

test_metric_2 = MetricsData([ResourceMetrics(Resource({"name": "test"}),
                                             [ScopeMetrics(InstrumentationScope(""),
                                                           [Metric("", "", "",
                                                                   Gauge([NumberDataPoint({}, 1, 2, 2),
                                                                          NumberDataPoint({}, 1, 2, 2.0)]))],
                                                           "")],
                                             "")])

test_metric_3 = MetricsData([ResourceMetrics(Resource({"name": "test"}),
                                             [ScopeMetrics(InstrumentationScope(""),
                                                           [Metric("", "", "",
                                                                   Histogram([HistogramDataPoint({}, 2, 3, 1, 1, [1],
                                                                                                 [1], 1, 1)], 0))],
                                                           "")],
                                             "")])


class TestMetricExporter(unittest.TestCase):
    def test_export(self):
        self.assertEqual(metric_exporter.export(test_metric_1), MetricExportResult.SUCCESS)
        self.assertEqual(metric_exporter.export(test_metric_2), MetricExportResult.SUCCESS)
        self.assertEqual(metric_exporter.export(test_metric_3), MetricExportResult.SUCCESS)

    def test_force_flush(self):
        self.assertEqual(metric_exporter.force_flush(), False)

    def test_shutdown(self):
        self.assertIsNone(metric_exporter.shutdown())

    def test_export_metrics(self):
        self.assertEqual(metric_exporter.export_metrics(test_metric_1), False)


if __name__ == "__main__":
    unittest.main()
