#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import benchmark

from tlogging import SamplerLogger, span
from tlogging import Metrics
from tlogging.field import Events, Attributes, ExternalSpans
from tlogging.tencode import Encoder

RUNS = 500
_VSESION = "AISHUV0"
NULL = '/dev/null'


class TestTlogger(benchmark.Benchmark):
    each = RUNS  # allows for differing number of runs

    def setUp(self):
        self.size = 2500
        self.logger = SamplerLogger()
        self.logger.loglevel = "AllLevel"
        self.span = self.logger.internal_span()
        self.m1 = Metrics()
        self.m1.set_attributes("1", "2")
        self.m1.set_attributes("2", "3")
        self.m1.set_label("lll")
        self.test = []
        self.stdout = sys.stdout
        f = open('nul', 'w')
        if sys.platform.startswith("linux"):
            f = open(NULL, 'w')
        sys.stdout = f

    def tearDown(self):
        self.test = None
        del self.span
        sys.stdout = self.stdout

    def test_create_internal_span(self):
        # a = self.logger.internal_span()
        self.test.append(self.logger.internal_span())

    def test_create_children_span(self):
        self.test.append(self.logger.children_span(self.span))

    def test_add_logger_info(self):
        self.logger.debug("ahah", self.span)

    def test_set_tarceid(self):
        self.logger.set_tarceid("sss", self.span)

    def test_set_metrics(self):
        self.logger.set_metrics(self.m1, self.span)

    def test_set_parentid(self):
        self.logger.set_parentid("test", self.span)

    def test_gen_id(self):
        self.logger.gen_id()

    def test_set_attributes(self):
        self.logger.set_attributes("test", {"user.id": "01", "act.type": "search topic", "user.dep": "011",
                                            "act.keyword": "建筑"}, self.span)

    def test__get_level(self):
        self.logger._get_level()


class TestSpan(benchmark.Benchmark):
    each = RUNS

    def setUp(self):
        self.encoder = Encoder().tprint
        self.span = span.InternalSpan(version=_VSESION, parent_id="", trace_id="123123",
                                      span_id="123123", outer_func=self.encoder)
        self.metrics = Metrics()
        self.metrics.set_attributes("1", "2")
        self.metrics.set_attributes("2", "3")
        self.metrics.set_label("lll")
        self.eventes = Events("Debug", "hahahh, test")
        self.attributes = Attributes("test", {"ssss": 1})
        self.external = ExternalSpans()
        self.stdout = sys.stdout
        f = open('nul', 'w')
        if sys.platform.startswith("linux"):
            f = open('/dev/null', 'w')
        sys.stdout = f

    def tearDown(self):
        self.test = None
        del self.span
        sys.stdout = self.stdout

    def test__set_version(self):
        self.span._set_version("test")

    def test__set_trance_id(self):
        self.span._set_trance_id("sss")

    def test__get_span_id(self):
        self.span._get_span_id()

    def test__get_trace_id(self):
        self.span._get_trace_id()

    def test__set_span_id(self):
        self.span._set_span_id("sss")

    def test__set_parent_id(self):
        self.span._set_parent_id("sss")

    def test__set_outer(self):
        self.span._set_outer(self.encoder)

    def test__set_attributes(self):
        self.span._set_attributes(self.attributes)

    def test__set_metrics(self):
        self.span._set_metrics(self.metrics)

    def test__set_events(self):
        self.span._set_events(self.eventes)

    def test__init_body(self):
        self.span._init_body()

    def test__set_end(self):
        self.span._set_end()

    def test__get_time(self):
        self.span._get_time()


class TestFieldMetrics(benchmark.Benchmark):
    each = RUNS

    def setUp(self):
        self.metrics = Metrics()

    def test_set_attributes(self):
        self.metrics.set_attributes("1", "2")

    def test_set_other_property(self):
        self.metrics.set_other_property("1", "2")

    def test_set_label(self):
        self.metrics.set_label("1")

    def test_get_all_property(self):
        self.metrics.get_all_property()


class TestTencode(benchmark.Benchmark):
    each = RUNS

    def setUp(self):
        self.encoder = Encoder("json")
        self.stdout = sys.stdout
        f = open('nul', 'w')
        if sys.platform.startswith("linux"):
            f = open(NULL, 'w')
        sys.stdout = f

    def tearDown(self):
        sys.stdout = self.stdout

    def test_set_encoder(self):
        self.encoder.set_encoder("json")

    def test_tprint(self):
        self.encoder.tprint({1: 2, 3: 4})

    def test__encode_to_json(self):
        self.encoder._encode_to_json({1: 2, 3: 4})


if __name__ == '__main__':
    benchmark.main(format="markdown", numberFormat="%.4g")
