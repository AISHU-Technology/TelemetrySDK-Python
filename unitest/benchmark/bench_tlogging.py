#!/usr/bin/env python
# -*- coding: utf-8 -*-
from exporter.resource.resource import log_resource
from tlogging import SamplerLogger


def test_log_info(benchmark):
    logger = SamplerLogger(log_resource())
    logger.loglevel = "AllLevel"
    benchmark(logger.info, "test")
    logger.shutdown()


def test_log_warn(benchmark):
    logger = SamplerLogger(log_resource())
    logger.loglevel = "AllLevel"
    benchmark(logger.warn, "test")
    logger.shutdown()


def test_log_error(benchmark):
    logger = SamplerLogger(log_resource())
    logger.loglevel = "AllLevel"
    benchmark(logger.error, "test")
    logger.shutdown()


def test_log_debug(benchmark):
    logger = SamplerLogger(log_resource())
    logger.loglevel = "AllLevel"
    benchmark(logger.debug, "test")
    logger.shutdown()


def test_log_trace(benchmark):
    logger = SamplerLogger(log_resource())
    logger.loglevel = "AllLevel"
    benchmark(logger.trace, "test")
    logger.shutdown()


if __name__ == "__main__":
    pass
