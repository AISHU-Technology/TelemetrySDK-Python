import unittest

from exporter.ar_log.log_exporter import ARLogExporter
from exporter.public.client import StdoutClient
from tlogging.field import Body
from tlogging.processor import Processor
from tlogging.span import LogSpan

log_exporter = ARLogExporter(StdoutClient())
_span_processor = Processor({"Console": log_exporter})
span = LogSpan(_span_processor, Body("test"), "test", ctx=None, attributes=None, resources=None)
spans = [span]


class TestLogExporter(unittest.TestCase):
    def test_name(self):
        self.assertEqual(log_exporter.name(), "./AnyRobotData.txt")

    def test_shutdown(self):
        self.assertIsNone(log_exporter.shutdown())

    def test_export_logs(self):
        self.assertEqual(log_exporter.export_logs(spans), False)
