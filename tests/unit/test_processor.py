#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/18 10:24
# @Author  : Jimmy.li
# @Email   : jimmy.li@aishu.cn

import unittest

from tlogging.processor import Processor
from tlogging.exporter import ConsoleExporter

class TestProcess(unittest.TestCase):

    def setUp(self):
        self.exporter = ConsoleExporter()


    def test_shutdown(self):
        self.span_processor = Processor(self.exporter)
        self.span_processor.shutdown()

    def test__export(self):
        self.span_processor = Processor(self.exporter)
        self.span_processor.queue.append("xxxx")
        self.span_processor._export()

        self.span_processor = Processor(self.exporter, max_queue_size=2,max_span_list_size=1)
        self.span_processor.queue.append("xxxx")
        self.span_processor._export()



    def test__drain_queue(self):
        self.span_processor = Processor(self.exporter)
        self.span_processor.queue.append("xxxx")
        self.span_processor._drain_queue()

    def test_init_err(self):
        self.assertRaises(ValueError, Processor,self.exporter,max_queue_size=0)
        self.assertRaises(ValueError, Processor,self.exporter,max_span_list_size=0)
        self.assertRaises(ValueError, Processor,self.exporter,max_queue_size=1,max_span_list_size=2)