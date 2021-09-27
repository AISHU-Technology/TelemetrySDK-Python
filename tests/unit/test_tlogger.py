#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import allure

from tlogging import tlogger
from tlogging.field import Attributes
from tlogging.texception import TException


class TestTlogger(unittest.TestCase):

    def setUp(self):
        self.logger = tlogger.SamplerLogger()
        self.logger.loglevel = "TraceLevel"

    @allure.title("tlogging设置trace级别日志: 缺省etype, message为非str,设置失败; 缺省etype,message为str,设置成功; "
                  "设置etype, message为非str,设置成功; 设置etype，etype类型为非str，设置失败；"
                  "设置attributes，attributes类型为Attributes，设置成功")
    def test_trace(self):
        self.assertIsNone(self.logger.trace("sss"))
        self.assertIsNone(self.logger.trace("sss", etype="123"))
        self.assertIsNone(self.logger.trace("sss", attributes=Attributes("test attributes", "test")))
        self.assertRaises(TException, self.logger.trace, ["sss"])
        self.assertRaises(TException, self.logger.trace, "sss", etype=123)

    @allure.title("tlogging设置debug级别日志: 设置成功")
    def test_debug(self):
        self.assertIsNone(self.logger.debug("sss"))

    @allure.title("tlogging设置info级别日志: 设置成功")
    def test_info(self):
        self.assertIsNone(self.logger.info("sss"))

    @allure.title("tlogging设置warn级别日志:设置成功")
    def test_warn(self):
        self.assertIsNone(self.logger.warn("sss"))

    @allure.title("tlogging设置error级别日志: 设置成功")
    def test_error(self):
        self.assertIsNone(self.logger.error("sss"))

    @allure.title("tlogging设置fatal级别日志: 设置成功")
    def test_fatal(self):
        self.assertIsNone(self.logger.fatal("sss"))

    @allure.title("tlogging设置日志级别: 日志级别非法, 修改不成功,日志级别为默认级别")
    def test__get_level(self):
        self.logger.loglevel = "ssss"
        self.assertTrue(self.logger._get_level(), 3)
