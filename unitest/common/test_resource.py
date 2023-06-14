import unittest
from exporter.resource import resource
from exporter.resource.resource import default_service_name, inner_attributes, metric_resource, set_service_info, \
    trace_resource, log_resource


class TestResource(unittest.TestCase):
    def test_default_service_name(self):
        self.assertIsNotNone(default_service_name())

    def test_set_service_info(self):
        set_service_info(name="test_name", version="test_version", instance_id="test_instance_id")
        self.assertEqual(resource.global_service_name, "test_name")
        self.assertEqual(resource.global_service_version, "test_version")
        self.assertEqual(resource.global_service_instance_id, "test_instance_id")

    def test_inner_attributes(self):
        self.assertIsNotNone(inner_attributes())

    def test_trace_resource(self):
        self.assertIsNotNone(trace_resource())

    def test_log_resource(self):
        self.assertIsNotNone(log_resource())

    def test_metric_resource(self):
        self.assertIsNotNone(metric_resource())


if __name__ == "__main__":
    unittest.main()
