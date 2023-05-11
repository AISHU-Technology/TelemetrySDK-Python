import unittest

from opentelemetry.trace import StatusCode

from exporter.common.ar_trace import convert_status_code_to_golang


class TestARMetric(unittest.TestCase):
    def test_anyrobot_traces_from_trace_spans(self):
        pass

    def test_anyrobot_trace_from_trace(self):
        pass

    def test_anyrobot_span_context_from_context(self):
        pass

    def test_anyrobot_link_from_link(self):
        pass

    def test_anyrobot_event_from_event(self):
        pass

    def test_anyrobot_status_from_status(self):
        self.assertEqual(anyrobot_status_from_status(),1)
        pass

    def test_convert_status_code_to_golang(self):
        self.assertEqual(convert_status_code_to_golang(StatusCode(0)), 0)
        self.assertEqual(convert_status_code_to_golang(StatusCode(1)), 2)
        self.assertEqual(convert_status_code_to_golang(StatusCode(2)), 1)

