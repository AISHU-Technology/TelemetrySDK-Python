#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import ReadableSpan, Span
from opentelemetry.sdk.util.instrumentation import InstrumentationInfo, InstrumentationScope
from opentelemetry.trace import Status, StatusCode

from exporter.ar_metric.metric_exporter import ARMetricExporter
from exporter.ar_trace.trace_exporter import ARTraceExporter, tracer
from exporter.public.client import StdoutClient
from tlogging.exporter import ConsoleExporter
from tlogging.processor import Processor
from tlogging.span import LogSpan
from tlogging.field import Body
from opentelemetry import trace as trace_api

trace_exporter = ARTraceExporter(StdoutClient())


def test_trace_exporter_export(benchmark):
    # benchmark(trace_exporter.export(["test_trace"]))
    pass


def test_log_exporter_export(benchmark):
    log_exporter = ConsoleExporter()
    _span_processor = Processor({"Console": log_exporter})
    span = LogSpan(_span_processor, Body("test"), "test", ctx=None, attributes=None, resources=None)
    spans = [span]

    def benchmark_log_exporter_export():
        log_exporter.export(spans)

    benchmark(benchmark_log_exporter_export)
    _span_processor.shutdown()


metric_exporter = ARMetricExporter(StdoutClient())


def test_metric_exporter_export(benchmark):
    # benchmark(metric_exporter.export("metrics_data"))
    pass


if __name__ == "__main__":
    pass
