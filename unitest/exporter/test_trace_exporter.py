import unittest

from opentelemetry.sdk.trace import SynchronousMultiSpanProcessor, TracerProvider, ReadableSpan
from opentelemetry.sdk.trace.export import SpanExportResult, BatchSpanProcessor
from opentelemetry.sdk.util.instrumentation import InstrumentationScope
from opentelemetry.trace import set_tracer_provider, SpanContext, Link

from exporter.ar_trace.trace_exporter import ARTraceExporter, tracer
from exporter.public.client import StdoutClient
from exporter.resource.resource import trace_resource


class SelfDict(dict):
    def __init__(self):
        super(SelfDict, self).__init__()
        self.dropped = 0


class SelfLink(list):
    def __init__(self, seq=()):
        super(SelfLink, self).__init__(seq)
        self.dropped = 0


trace_exporter = ARTraceExporter(StdoutClient())
test_attribute = SelfDict()
test_context = SpanContext.__new__(SpanContext, 0, 0, False)
test_trace_1 = ReadableSpan(attributes=test_attribute, instrumentation_scope=InstrumentationScope(name="test"))
test_trace_2 = ReadableSpan(attributes=test_attribute, instrumentation_scope=InstrumentationScope(name="test"),
                            context=test_context, links=SelfLink([Link(test_context, test_attribute)]))


class TestTraceExporter(unittest.TestCase):
    def test_export(self):
        self.assertEqual(trace_exporter.export([test_trace_1]), SpanExportResult.SUCCESS)
        pass

    def test_force_flush(self):
        self.assertEqual(trace_exporter.force_flush(), False)

    def test_shutdown(self):
        self.assertIsNone(trace_exporter.shutdown())

    def test_export_traces(self):
        self.assertEqual(trace_exporter.export_traces([test_trace_2]), False)
        pass


if __name__ == "__main__":
    unittest.main()
