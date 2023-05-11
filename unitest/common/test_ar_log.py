import unittest
from exporter.common.ar_log import anyrobot_logs_from_logs
from tlogging.exporter import ConsoleExporter
from tlogging.field import Body
from tlogging.processor import Processor
from tlogging.span import LogSpan


class TestARLog(unittest.TestCase):
    def test_anyrobot_logs_from_logs(self):
        log_exporter = ConsoleExporter()
        _span_processor = Processor({"Console": log_exporter})
        span = LogSpan(_span_processor, Body("test"), "test", ctx=None, attributes=None, resources=None)
        spans = [span]
        self.assertIsNotNone(anyrobot_logs_from_logs(spans))
