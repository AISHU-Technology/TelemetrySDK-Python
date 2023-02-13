import unittest

from exporter.resource.resource import default_service_name, inner_attributes, metric_resource


class TestResource(unittest.TestCase):
    def test_default_service_name(self):
        self.assertIsNotNone(default_service_name())

    def test_inner_attributes(self):
        self.assertIsNotNone(inner_attributes())

    def test_metric_resource(self):
        self.assertIsNotNone(metric_resource())
