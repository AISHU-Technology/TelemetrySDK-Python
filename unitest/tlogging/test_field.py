#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from tlogging import field


class TestFieldAttributes(unittest.TestCase):

    def test_get_all_property(self):
        attributes = field.Attributes("test", "ssss")
        self.assertTrue(attributes.all_property, {'test': 'ssss', 'type': 'test'})


class TestFieldResources(unittest.TestCase):

    def setUp(self):
        self.resources = field.Resources({})

    def test_get_all_property(self):
        self.assertIsNotNone(self.resources.all_property)


class TestFieldBody(unittest.TestCase):

    def test_set_type(self):
        self.body = field.Body("test log 1")
        self.assertIsNone(self.body.set_type("test"))

    def test_set_message(self):
        self.body = field.Body("test log 2", "test")
        self.assertIsNone(self.body.set_message({"a": 1, "b": 2}))

    def test_all_property(self):
        self.body = field.Body("test log 3", "test")
        self.assertTrue(self.body.all_property, {'Message': 'test log'})


if __name__ == "__main__":
    unittest.main()
