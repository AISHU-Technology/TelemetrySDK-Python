#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import allure

from tlogging import tlogger
from tlogging import span
from tlogging.field import Metrics
from tlogging.texception import TException


class TestTlogger(unittest.TestCase):

    def setUp(self):
        self.logger = tlogger.SamplerLogger()
        self.logger.loglevel = "AllLevel"

    @allure.title("tlogging创建span: 创建成功")
    def test_internal_span(self):
        self.assertIsInstance(self.logger.internal_span(), span.InternalSpan)

    @allure.title("tlogging创建子span: 子span传入的span不存在,创建失败; 子span传入的span存在,创建成功,上下文关系正常")
    def test_children_span(self):
        my_span = self.logger.internal_span()
        span_id = my_span._get_span_id()
        children = self.logger.children_span(my_span)
        parent_id = children._InternalSpan__parent_id
        self.assertTrue(span_id, parent_id)
        self.assertRaises(TException, self.logger.children_span, "sss")

    @allure.title("tlogging设置traceid: 传入的span不存在,修改失败; 传入的span存在,修改成功")
    def test_set_tarceid(self):
        span = self.logger.internal_span()
        self.assertIsNone(self.logger.set_tarceid("sss", span))
        self.assertRaises(TException, self.logger.set_tarceid, "sss", "sss1")

    @allure.title("tlogging设置metrics: 传入的span不存在,设置失败; 传入的metrics类型错误,设置失败; 传入的span存在,设置成功")
    def test_set_metrics(self):
        span = self.logger.internal_span()
        m1 = Metrics()
        m1.set_attributes("1", "2")
        m1.set_attributes("2", "3")
        m1.set_label("lll")
        self.assertIsNone(self.logger.set_metrics(m1, span))
        self.assertRaises(TException, self.logger.set_metrics, "sss", "sss1")
        self.assertRaises(TException, self.logger.set_metrics, m1, "sss1")

    @allure.title("tlogging设置parentid: 传入的span不存在,设置失败; 传入的span存在,设置成功")
    def test_set_parentid(self):
        span = self.logger.internal_span()
        self.assertIsNone(self.logger.set_parentid("sss", span))
        self.assertRaises(TException, self.logger.set_parentid, "sss", "sss1")

    @allure.title("tlogging生成id: 生成成功")
    def test_gen_id(self):
        self.assertIsNotNone(self.logger.gen_id())

    @allure.title("tlogging设置attributes: span不存在,设置失败; 重复修改,成功; 传入的span存在,设置成功")
    def test_set_attributes(self):
        span = self.logger.internal_span()
        self.assertRaises(TException, self.logger.set_attributes, "test", {"user.id": "01", "act.type": "search topic",
                                                                           "user.dep": "011", "act.keyword": "建筑"},
                          "123")
        self.assertIsNone(self.logger.set_attributes("test", {"user.id": "01", "act.type": "search topic",
                                                              "user.dep": "011", "act.keyword": "建筑"}, span))
        self.assertIsNone(self.logger.set_attributes("test", {"user.id": "01"}, span))
        self.assertIsNone(self.logger.set_attributes("test", "sss", span))

    @allure.title("tlogging设置tarce级别日志: span不存在,设置失败; 缺省etype, message为非str,设置失败; 缺省etype,"
                  " message为str,设置成功; 设置etype, message为非str,设置成功; 传入的span存在,设置成功")
    def test_trace(self):
        span = self.logger.internal_span()
        self.assertRaises(TException, self.logger.trace, "sss", "123")
        self.assertIsNone(self.logger.trace("sss", span))
        self.assertIsNone(self.logger.trace(["sss"], span, "test"))
        self.assertRaises(TException, self.logger.trace, ["sss"], span)
        self.assertRaises(TException, self.logger.trace, "sss", span, 123)

    @allure.title("tlogging设置debug级别日志: span不存在,设置失败; 传入的span存在,设置成功")
    def test_debug(self):
        span = self.logger.internal_span()
        self.assertRaises(TException, self.logger.debug, "sss", "123")
        self.assertIsNone(self.logger.debug("sss", span))

    @allure.title("tlogging设置info级别日志: span不存在,设置失败; 传入的span存在,设置成功")
    def test_info(self):
        span = self.logger.internal_span()
        self.assertRaises(TException, self.logger.info, "sss", "123")
        self.assertIsNone(self.logger.info("sss", span))

    @allure.title("tlogging设置warn级别日志: span不存在,设置失败; 传入的span存在,设置成功")
    def test_warn(self):
        span = self.logger.internal_span()
        self.assertRaises(TException, self.logger.warn, "sss", "123")
        self.assertIsNone(self.logger.warn("sss", span))

    @allure.title("tlogging设置error级别日志: span不存在,设置失败; 传入的span存在,设置成功")
    def test_error(self):
        span = self.logger.internal_span()
        self.assertRaises(TException, self.logger.error, "sss", "123")
        self.assertIsNone(self.logger.error("sss", span))

    @allure.title("tlogging设置fatal级别日志: span不存在,设置失败; 传入的span存在,设置成功")
    def test_fatal(self):
        span = self.logger.internal_span()
        self.assertRaises(TException, self.logger.fatal, "sss", "123")
        self.assertIsNone(self.logger.fatal("sss", span))

    @allure.title("tlogging释放span: 先释放部分span,在释放全部span,无重复span输出")
    def test_close(self):
        span = self.logger.internal_span()
        span.signal()
        self.assertIsNone(self.logger.close())

    @allure.title("tlogging设置日志级别: 日志级别非法, 修改不成功,日志级别为默认级别")
    def test__get_level(self):
        self.logger.loglevel = "ssss"
        self.assertTrue(self.logger._get_level(), 3)
