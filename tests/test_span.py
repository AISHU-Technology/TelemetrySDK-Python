#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from tlogging import span
from tlogging.field import Attributes, Metrics, Events, ExternalSpans
from tlogging.tencode import Encoder
from tlogging.texception import TException

_VSESION = "AISHUV0"


class TestSpan(unittest.TestCase):

    def setUp(self):
        encoder = Encoder().tprint
        self.span = span.InternalSpan(version=_VSESION, parent_id="", trace_id="123123",
                                      span_id="123123", outer_func=encoder)

    def test__set_version(self):
        self.assertRaises(TException, self.span._set_version, 123213)
        self.assertIsNone(self.span._set_version("32123"))

    def test__set_trance_id(self):
        self.assertRaises(TException, self.span._set_trance_id, 123213)
        self.assertIsNone(self.span._set_trance_id("32123"))

    def test__get_span_id(self):
        self.assertTrue(self.span._get_span_id(), "123123")

    def test__set_span_id(self):
        self.assertRaises(TException, self.span._set_span_id, 123213)
        self.assertIsNone(self.span._set_span_id("32123"))

    def test__set_parent_id(self):
        self.assertRaises(TException, self.span._set_parent_id, 123213)
        self.assertIsNone(self.span._set_parent_id("32123"))

    def test__set_outer(self):
        self.assertRaises(TException, self.span._set_outer, 123213)
        self.assertIsNone(self.span._set_outer(Encoder().tprint))

    def test__set_attributes(self):
        self.assertRaises(TException, self.span._set_attributes, 123213)
        self.assertIsNone(self.span._set_attributes(Attributes("test", "ssss")))

    def test__set_metrics(self):
        m1 = Metrics()
        m1.set_attributes("1", "2")
        m1.set_attributes("2", "3")
        m1.set_label("lll")
        self.assertRaises(TException, self.span._set_metrics, 123213)
        self.assertIsNone(self.span._set_metrics(m1))

    def test__set_events(self):
        self.assertRaises(TException, self.span._set_events, 123213)
        self.assertIsNone(self.span._set_events(Events("Debug", "hahahh, test")))

    def test__set_external_spans(self):
        self.assertRaises(TException, self.span._set_external_spans, 123213)
        self.assertIsNone(self.span._set_external_spans(ExternalSpans()))

    def test_signal(self):
        self.assertIsNone(self.span.signal())

    def test__init_body(self):
        self.assertIsNone(self.span._init_body())

    def test__set_end(self):
        self.assertIsNone(self.span._set_end())

    def test__get_time(self):
        self.assertIsNotNone(self.span._get_time())
