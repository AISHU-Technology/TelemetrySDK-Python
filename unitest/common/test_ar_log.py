import unittest
from exporter.common.ar_log import anyrobot_logs_from_logs
from tlogging.exporter import ConsoleExporter
from tlogging.field import Body
from tlogging.processor import Processor
from tlogging.span import LogSpan


class TestARLog(unittest.TestCase):
    def setUp(self):
        self.exporters = {"Console": ConsoleExporter()}
        self.span_processor = Processor(self.exporters)

    def tearDown(self):
        self.span_processor.shutdown()

    def test_anyrobot_logs_from_logs(self):
        span = LogSpan(self.span_processor, Body("test"), "test", ctx=None, attributes=None, resources=None)
        spans = [span]
        self.assertIsNotNone(anyrobot_logs_from_logs(spans))


if __name__ == "__main__":
    unittest.main()
