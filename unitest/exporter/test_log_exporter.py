import unittest

from exporter.ar_log.log_exporter import ARLogExporter
from exporter.public.client import StdoutClient
from tlogging.field import Body
from tlogging.processor import Processor
from tlogging.span import LogSpan


class TestLogExporter(unittest.TestCase):
    def setUp(self):
        self.log_exporter = ARLogExporter(StdoutClient())
        self.span_processor = Processor({"Console": self.log_exporter})

    def tearDown(self):
        self.span_processor.shutdown()

    def test_name(self):
        self.assertEqual(self.log_exporter.name(), "./AnyRobotData.txt")

    def test_shutdown(self):
        self.assertIsNone(self.log_exporter.shutdown())

    def test_export_logs(self):
        span = LogSpan(self.span_processor, Body("test"), "test", ctx=None, attributes=None, resources=None)
        spans = [span]
        self.assertEqual(self.log_exporter.export_logs(spans), False)


if __name__ == "__main__":
    unittest.main()
