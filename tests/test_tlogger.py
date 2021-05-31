#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from tlogging import tlogger
from tlogging import span
from tlogging.field import Metrics
from tlogging.texception import TException


class TestTlogger(unittest.TestCase):

    def setUp(self):
        self.logger = tlogger.SamplerLogger()
        self.logger.loglevel = "AllLevel"

    def test_internal_span(self):
        self.assertIsInstance(self.logger.internal_span(), span.InternalSpan)

    def test_children_span(self):
        my_span = self.logger.internal_span()
        span_id = my_span._get_span_id()
        children = self.logger.children_span(my_span)
        parent_id = children._InternalSpan__parent_id
        self.assertTrue(span_id, parent_id)
        self.assertRaises(TException, self.logger.children_span, "sss")

    def test_set_tarceid(self):
        span = self.logger.internal_span()
        self.assertIsNone(self.logger.set_tarceid("sss", span))

    def test_set_metrics(self):
        span = self.logger.internal_span()
        m1 = Metrics()
        m1.set_attributes("1", "2")
        m1.set_attributes("2", "3")
        m1.set_label("lll")
        self.assertIsNone(self.logger.set_metrics(m1, span))

    def test_set_parentid(self):
        span = self.logger.internal_span()
        self.assertIsNone(self.logger.set_parentid("sss", span))

    def test_gen_id(self):
        self.assertIsNotNone(self.logger.gen_id())

    def test_set_attributes(self):
        span = self.logger.internal_span()
        self.assertRaises(TException, self.logger.set_attributes, "test", {"user.id": "01", "act.type": "search topic",
                                                                           "user.dep": "011", "act.keyword": "建筑"},
                          "123")
        self.assertIsNone(self.logger.set_attributes("test", {"user.id": "01", "act.type": "search topic",
                                                              "user.dep": "011", "act.keyword": "建筑"}, span))
        self.assertIsNone(self.logger.set_attributes("test", {"user.id": "01"}, span))
        self.assertIsNone(self.logger.set_attributes("test", "sss", span))

    def test_trace(self):
        span = self.logger.internal_span()
        self.assertRaises(TException, self.logger.trace, "sss", "123")
        self.assertIsNone(self.logger.trace("sss", span))
        self.assertIsNone(self.logger.trace(["sss"], span, "test"))
        self.assertRaises(TException, self.logger.trace, ["sss"], span)
        self.assertRaises(TException, self.logger.trace, "sss", span, 123)

    def test_debug(self):
        span = self.logger.internal_span()
        self.assertRaises(TException, self.logger.debug, "sss", "123")
        self.assertIsNone(self.logger.debug("sss", span))

    def test_info(self):
        span = self.logger.internal_span()
        self.assertRaises(TException, self.logger.info, "sss", "123")
        self.assertIsNone(self.logger.info("sss", span))

    def test_warn(self):
        span = self.logger.internal_span()
        self.assertRaises(TException, self.logger.warn, "sss", "123")
        self.assertIsNone(self.logger.warn("sss", span))

    def test_error(self):
        span = self.logger.internal_span()
        self.assertRaises(TException, self.logger.error, "sss", "123")
        self.assertIsNone(self.logger.error("sss", span))

    def test_fatal(self):
        span = self.logger.internal_span()
        self.assertRaises(TException, self.logger.fatal, "sss", "123")
        self.assertIsNone(self.logger.fatal("sss", span))

    def test_close(self):
        span = self.logger.internal_span()
        span.signal()
        self.assertIsNone(self.logger.close())

    def test__get_level(self):
        self.logger.loglevel = "ssss"
        self.assertTrue(self.logger._get_level(), 3)
