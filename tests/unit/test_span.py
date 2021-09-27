#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from tlogging import span
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
