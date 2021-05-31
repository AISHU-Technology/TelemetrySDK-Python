#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from tlogging import tencode
from tlogging.texception import TException


class TestTencode(unittest.TestCase):

    def setUp(self):
        self.encoder = tencode.Encoder()

    def test_set_encoder(self):
        self.assertRaises(TException, self.encoder.set_encoder, "sss")
        self.assertIsNone(self.encoder.set_encoder("json"))

    def test_tprint(self):
        self.assertIsNone(self.encoder.tprint("test"))

    def test__encode_to_json(self):
        self.assertRaises(TException, self.encoder._encode_to_json, {1, 2, 3})
        self.assertIsNotNone(self.encoder._encode_to_json("123132123"))
