#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from tlogging import field
from tlogging.texception import TException


class TestFieldMetrics(unittest.TestCase):

    def setUp(self):
        self.metrics = field.Metrics()

    def test_set_attributes(self):
        self.assertRaises(TException, self.metrics.set_attributes, 1, 2)
        self.assertRaises(TException, self.metrics.set_attributes, "1", 2)
        self.assertIsNone(self.metrics.set_attributes("1", "2"))

    def test_set_other_property(self):
        self.assertRaises(TException, self.metrics.set_other_property, 1, 2)
        self.assertRaises(TException, self.metrics.set_other_property, "1", 2)
        self.assertRaises(TException, self.metrics.set_other_property, "Attributes", "2")
        self.assertIsNone(self.metrics.set_other_property("1", "2"))

    def test_set_label(self):
        self.assertRaises(TException, self.metrics.set_label, 1)
        self.assertIsNone(self.metrics.set_label("1"))

    def test_get_all_property(self):
        self.metrics.set_other_property("1", "2")
        self.metrics.set_label("1")
        self.metrics.set_attributes("1", "2")
        self.assertTrue(self.metrics.get_all_property(), {'1': '2', 'Attributes': {'1': '2'}, 'Labels': ['1']})


class TestFieldEvents(unittest.TestCase):

    def setUp(self):
        self.events = field.Events("Debug", "hahahh, test")

    def test_get_all_property(self):
        self.assertIsNotNone(self.events.get_all_property)

    def test__get_time(self):
        self.assertIsNotNone(self.events._get_time())


class TestFieldAttributes(unittest.TestCase):

    def setUp(self):
        self.attributes = field.Attributes("test", "ssss")

    def test_set_type(self):
        self.assertRaises(TException, self.attributes.set_type, 123)
        self.assertIsNone(self.attributes.set_type("123"))

    def test_set_attributes(self):
        self.assertIsNone(self.attributes.set_attributes("123"))

    def test_get_all_property(self):
        self.assertTrue(self.attributes.get_all_property(), {'test': 'ssss', 'type': 'test'})


class TestFieldExternalSpans(unittest.TestCase):

    def setUp(self):
        self.external = field.ExternalSpans()

    def test_get_all_property(self):
        self.assertIsNone(self.external.get_all_property())


class TestFieldResources(unittest.TestCase):

    def setUp(self):
        self.resources = field.Resources()

    def test__get_hostname(self):
        self.assertIsNotNone(self.resources._get_hostname())

    def test_get_all_property(self):
        self.assertIsNotNone(self.resources.get_all_property())

