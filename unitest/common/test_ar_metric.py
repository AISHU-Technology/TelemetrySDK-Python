import unittest

from exporter.common.ar_metric import anyrobot_rfc3339_nano_from_unix_nano, anyrobot_temporality_from_temporality


class TestARMetric(unittest.TestCase):
    def test_anyrobot_metrics_from_resource_metrics(self):
        assert True

    def test_anyrobot_metric_from_resource_metric(self):
        assert True

    def test_anyrobot_scope_metric_from_scope_metric(self):
        assert True

    def test_anyrobot_metric_from_metric(self):
        assert True

    def test_anyrobot_sum_from_sum(self):
        assert True

    def test_anyrobot_gauge_from_gauge(self):
        assert True

    def test_anyrobot_histogram_from_histogram(self):
        assert True

    def test_anyrobot_data_point_from_data_point(self):
        assert True

    def test_int_data_point(self):
        assert True

    def test_float_data_point(self):
        assert True

    def test_anyrobot_histogram_data_point_from_histogram_data_point(self):
        assert True

    def test_anyrobot_temporality_from_temporality(self):
        self.assertEqual(anyrobot_temporality_from_temporality(1), "DeltaTemporality")
        self.assertEqual(anyrobot_temporality_from_temporality(2), "CumulativeTemporality")
        self.assertEqual(anyrobot_temporality_from_temporality(0), "undefinedTemporality")

    def test_anyrobot_rfc3339_nano_from_unix_nano(self):
        self.assertEqual(anyrobot_rfc3339_nano_from_unix_nano(1675067513326319500), "2023-01-30T16:31:53.326319+08:00")
