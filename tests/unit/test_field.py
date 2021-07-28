#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import allure

from tlogging import field
from tlogging.texception import TException


class TestFieldMetrics(unittest.TestCase):

    def setUp(self):
        self.metrics = field.Metrics()

    @allure.title("metrics设置attributes: key类型错误,失败; value类型错误,失败; key和value类型正确,成功")
    def test_set_attributes(self):
        self.assertRaises(TException, self.metrics.set_attributes, 1, 2)
        self.assertRaises(TException, self.metrics.set_attributes, "1", 2)
        self.assertIsNone(self.metrics.set_attributes("1", "2"))

    @allure.title("metrics设置自定义属性: key类型错误,失败; value类型错误,失败; 自定义属性为基本属性,"
                  "失败; key和value类型正确,成功")
    def test_set_other_property(self):
        self.assertRaises(TException, self.metrics.set_other_property, 1, 2)
        self.assertRaises(TException, self.metrics.set_other_property, "1", "2")
        self.assertRaises(TException, self.metrics.set_other_property, "Attributes", "2")
        self.assertIsNone(self.metrics.set_other_property("1", 2))

    @allure.title("metrics设置label: label值类型错误,失败; label值类型正确,成功")
    def test_set_label(self):
        self.assertRaises(TException, self.metrics.set_label, 1)
        self.assertIsNone(self.metrics.set_label("1"))

    @allure.title("获取metrics所有属性和值: 获取成功")
    def test_get_all_property(self):
        self.metrics.set_other_property("1", 2)
        self.metrics.set_label("1")
        self.metrics.set_attributes("1", "2")
        self.assertTrue(self.metrics.get_all_property(), {'1': '2', 'Attributes': {'1': '2'}, 'Labels': ['1']})


class TestFieldEvents(unittest.TestCase):

    def setUp(self):
        self.events = field.Events("Debug", "hahahh, test")

    @allure.title("获取events所有属性和值: 获取成功")
    def test_get_all_property(self):
        self.assertIsNotNone(self.events.get_all_property)

    @allure.title("events获取当前时间: 获取成功")
    def test__get_time(self):
        self.assertIsNotNone(self.events._get_time())


class TestFieldAttributes(unittest.TestCase):

    def setUp(self):
        self.attributes = field.Attributes("test", "ssss")

    @allure.title("attributes设置atype: atype类型错误,设置失败; atype类型正确, 设置成功")
    def test_set_type(self):
        self.assertRaises(TException, self.attributes.set_type, 123)
        self.assertIsNone(self.attributes.set_type("123"))

    @allure.title("attributes设置attributes值: 设置成功")
    def test_set_attributes(self):
        self.assertIsNone(self.attributes.set_attributes("123"))

    @allure.title("获取attributes所有属性和值: 获取成功")
    def test_get_all_property(self):
        self.assertTrue(self.attributes.get_all_property(), {'test': 'ssss', 'type': 'test'})


class TestFieldResources(unittest.TestCase):

    def setUp(self):
        self.resources = field.Resources()

    def test__get_hostname(self):
        self.assertIsNotNone(self.resources._get_hostname())

    def test_get_all_property(self):
        self.assertIsNotNone(self.resources.get_all_property())

