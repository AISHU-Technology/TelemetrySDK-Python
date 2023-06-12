import unittest
from unittest import mock

from opentelemetry.sdk.trace import Event
from opentelemetry.trace import StatusCode, Status

from exporter.common.ar_trace import convert_status_code_to_golang, anyrobot_status_from_status, \
    anyrobot_event_from_event


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
        self.assertEqual(anyrobot_event_from_event(mock.MagicMock()), 1)
        pass

    def test_anyrobot_status_from_status(self):
        self.assertEqual(anyrobot_status_from_status(Status()), '{"Code": 0, "Description": ""}')
        pass

    def test_convert_status_code_to_golang(self):
        self.assertEqual(convert_status_code_to_golang(StatusCode(0)), 0)
        self.assertEqual(convert_status_code_to_golang(StatusCode(1)), 2)
        self.assertEqual(convert_status_code_to_golang(StatusCode(2)), 1)
