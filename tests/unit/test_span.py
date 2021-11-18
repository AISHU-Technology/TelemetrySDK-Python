#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from tlogging import span
from tlogging.span import check_flag
from tlogging.field import Attributes, Body
from tlogging.exporter import ConsoleExporter
from tlogging.processor import Processor
from tlogging.texception import TException

_VERSION = "v1.6.1"


class TestSpan(unittest.TestCase):

    def setUp(self):
        exporter = ConsoleExporter()
        self.span_processor = Processor(exporter)
        self.body = Body("test log")
        self.severity_text = "warn"
        self.span = span.LogSpan(self.span_processor, self.body, self.severity_text, ctx=None, attributes=None)

    def test__gen_trance_id(self):
        self.assertIsNotNone(self.span._gen_trace_id())

    def test__gen_span_id(self):
        self.assertIsNotNone(self.span._gen_span_id())

    def test__set_attributes(self):
        self.assertRaises(TException, self.span.set_attributes, 123213)
        self.assertIsNone(self.span.set_attributes(Attributes("test", "ssss")))

    def test_end(self):
        self.assertIsNone(self.span.end())

    def test__get_time(self):
        self.assertIsNotNone(self.span._get_time())

    def test__readable_span(self):
        self.assertIsInstance(self.span._readable_span(), span._Span)

    def test_to_json(self):
        self.span.to_json()

    def test_info(self):
        span_info = span.LogSpan(self.span_processor, self.body, self.severity_text, ctx=None, attributes=Attributes("test", "ssss"))
        check_flag(span_info.version)
        self.assertIsNotNone(span_info.version)
        self.assertIsNotNone(span_info.trace_id)
        self.assertIsNotNone(span_info.span_id)
        self.assertIsNotNone(span_info.severity_text)
        self.assertIsNotNone(span_info.timestamp)
        self.assertIsNotNone(span_info.resources)
        self.assertIsNotNone(span_info.attributes)
        self.assertIsNotNone(span_info.body)
