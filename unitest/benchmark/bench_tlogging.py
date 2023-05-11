#!/usr/bin/env python
# -*- coding: utf-8 -*-
from exporter.resource.resource import log_resource
from tlogging import SamplerLogger

logger = SamplerLogger(log_resource())
logger.loglevel = "AllLevel"


def test_log_info(benchmark):
    benchmark(logger.info, "test")


def test_log_warn(benchmark):
    benchmark(logger.warn, "test")


def test_log_error(benchmark):
    benchmark(logger.error, "test")


def test_log_debug(benchmark):
    benchmark(logger.debug, "test")


def test_log_trace(benchmark):
    benchmark(logger.trace, "test")
