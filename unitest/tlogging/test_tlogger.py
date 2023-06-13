#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import allure

from exporter.resource.resource import log_resource
from tlogging import tlogger
from tlogging.exporter import ConsoleExporter
from tlogging.field import Attributes
from tlogging.texception import TException

attributes_content = "test attributes"


class TestSamplerLogger(unittest.TestCase):

    def setUp(self):
        self.logger = tlogger.SamplerLogger(log_resource())
        self.logger.shutdown()
        self.logger = tlogger.SamplerLogger(log_resource(), ConsoleExporter())
        self.logger.loglevel = "TraceLevel"

    def tearDown(self):
        self.logger.shutdown()

    @allure.title("tlogging设置trace级别日志: 缺省etype, message为非str,设置失败; 缺省etype,message为str,设置成功; "
                  "设置etype, message为非str,设置成功; 设置etype，etype类型为非str，设置失败；"
                  "设置attributes，attributes类型为Attributes，设置成功")
    def test_trace(self):
        self.assertIsNone(self.logger.trace("sss"))
        self.assertIsNone(self.logger.trace("sss", etype="123"))
        self.assertIsNone(self.logger.trace("sss", attributes=Attributes(attributes_content, "test")))
        self.assertRaises(TException, self.logger.trace, ["sss"])
        self.assertRaises(TException, self.logger.trace, "sss", etype=123)
        self.assertRaises(TException, self.logger.trace, "sss", attributes={"aaa"})
        self.logger.loglevel = "FatalLevel"
        self.assertIsNone(self.logger.trace("sss", attributes=Attributes(attributes_content, "test")))

    @allure.title("tlogging设置debug级别日志: 设置成功")
    def test_debug(self):
        self.assertIsNone(self.logger.debug("sss", attributes=Attributes(attributes_content, "test")))
        self.assertRaises(TException, self.logger.debug, "sss", attributes={"aaa"})
        self.logger.loglevel = "FatalLevel"
        self.assertIsNone(self.logger.debug("sss", attributes=Attributes(attributes_content, "test")))

    @allure.title("tlogging设置info级别日志: 设置成功")
    def test_info(self):
        self.assertIsNone(self.logger.info("sss", attributes=Attributes(attributes_content, "test")))
        self.assertRaises(TException, self.logger.info, "sss", attributes={"aaa"})
        self.logger.loglevel = "FatalLevel"
        self.assertIsNone(self.logger.info("sss", attributes=Attributes(attributes_content, "test")))

    @allure.title("tlogging设置warn级别日志:设置成功")
    def test_warn(self):
        self.assertIsNone(self.logger.warn("sss", attributes=Attributes(attributes_content, "test")))
        self.assertRaises(TException, self.logger.warn, "sss", attributes={"aaa"})
        self.logger.loglevel = "FatalLevel"
        self.assertIsNone(self.logger.warn("sss", attributes=Attributes(attributes_content, "test")))

    @allure.title("tlogging设置error级别日志: 设置成功")
    def test_error(self):
        self.assertIsNone(self.logger.error("sss", attributes=Attributes(attributes_content, "test")))
        self.assertRaises(TException, self.logger.error, "sss", attributes={"aaa"})
        self.logger.loglevel = "FatalLevel"
        self.assertIsNone(self.logger.error("sss", attributes=Attributes(attributes_content, "test")))

    @allure.title("tlogging设置fatal级别日志: 设置成功")
    def test_fatal(self):
        self.assertIsNone(self.logger.fatal("sss", attributes=Attributes(attributes_content, "test")))
        self.assertRaises(TException, self.logger.fatal, "sss", attributes={"aaa"})
        self.logger.loglevel = "FatalLevel"
        self.assertIsNone(self.logger.fatal("sss", attributes=Attributes(attributes_content, "test")))

    @allure.title("tlogging设置日志级别: 日志级别非法, 修改不成功,日志级别为默认级别")
    def test__get_level(self):
        self.logger.loglevel = "ssss"
        self.assertIsNone(self.logger._get_level())

    def test_shutdown(self):
        self.logger.shutdown()


class TestSyncLogger(unittest.TestCase):

    def setUp(self):
        self.logger = tlogger.SyncLogger(log_resource(), exporter=None)
        self.logger.shutdown()
        self.logger = tlogger.SyncLogger(log_resource(), ConsoleExporter())
        self.logger.loglevel = "TraceLevel"

    def tearDown(self):
        self.logger.shutdown()

    @allure.title("tlogging设置trace级别日志: 缺省etype, message为非str,设置失败; 缺省etype,message为str,设置成功; "
                  "设置etype, message为非str,设置成功; 设置etype，etype类型为非str，设置失败；"
                  "设置attributes，attributes类型为Attributes，设置成功")
    def test_trace(self):
        self.assertIsNotNone(self.logger.trace("sss"))
        self.assertIsNotNone(self.logger.trace("sss", etype="123"))
        self.assertIsNotNone(self.logger.trace("sss", attributes=Attributes(attributes_content, "test")))
        self.assertRaises(TException, self.logger.trace, ["sss"])
        self.assertRaises(TException, self.logger.trace, "sss", etype=123)
        self.assertRaises(TException, self.logger.trace, "sss", attributes={"aaa"})
        self.logger.loglevel = "FatalLevel"
        self.assertEqual(self.logger.trace("sss", attributes=Attributes(attributes_content, "test")), False)

    @allure.title("tlogging设置debug级别日志: 设置成功")
    def test_debug(self):
        self.assertIsNotNone(self.logger.debug("sss", attributes=Attributes(attributes_content, "test")))
        self.assertRaises(TException, self.logger.debug, "sss", attributes={"aaa"})
        self.logger.loglevel = "FatalLevel"
        self.assertEqual(self.logger.debug("sss", attributes=Attributes(attributes_content, "test")), False)

    @allure.title("tlogging设置info级别日志: 设置成功")
    def test_info(self):
        self.assertIsNotNone(self.logger.info("sss", attributes=Attributes(attributes_content, "test")))
        self.assertRaises(TException, self.logger.info, "sss", attributes={"aaa"})
        self.logger.loglevel = "FatalLevel"
        self.assertEqual(self.logger.info("sss", attributes=Attributes(attributes_content, "test")), False)

    @allure.title("tlogging设置warn级别日志:设置成功")
    def test_warn(self):
        self.assertIsNotNone(self.logger.warn("sss", attributes=Attributes(attributes_content, "test")))
        self.assertRaises(TException, self.logger.warn, "sss", attributes={"aaa"})
        self.logger.loglevel = "FatalLevel"
        self.assertEqual(self.logger.warn("sss", attributes=Attributes(attributes_content, "test")), False)

    @allure.title("tlogging设置error级别日志: 设置成功")
    def test_error(self):
        self.assertIsNotNone(self.logger.error("sss", attributes=Attributes(attributes_content, "test")))
        self.assertRaises(TException, self.logger.error, "sss", attributes={"aaa"})
        self.logger.loglevel = "FatalLevel"
        self.assertEqual(self.logger.error("sss", attributes=Attributes(attributes_content, "test")), False)

    @allure.title("tlogging设置fatal级别日志: 设置成功")
    def test_fatal(self):
        self.assertIsNotNone(self.logger.fatal("sss", attributes=Attributes(attributes_content, "test")))
        self.assertRaises(TException, self.logger.fatal, "sss", attributes={"aaa"})
        self.logger.loglevel = "FatalLevel"
        self.assertEqual(self.logger.fatal("sss", attributes=Attributes(attributes_content, "test")), False)

    @allure.title("tlogging设置日志级别: 日志级别非法, 修改不成功,日志级别为默认级别")
    def test__get_level(self):
        self.logger.loglevel = "ssss"
        self.assertIsNone(self.logger._get_level())

    def test_shutdown(self):
        self.logger.shutdown()


if __name__ == "__main__":
    unittest.main()
