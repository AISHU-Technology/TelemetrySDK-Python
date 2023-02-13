#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tlogging.exporter import ConsoleExporter
from tlogging.processor import Processor
from tlogging.span import LogSpan
from tlogging.field import Body


exporter = ConsoleExporter()
_span_processor = Processor(exporter)
span = LogSpan(_span_processor, Body("test"), "test", ctx=None, attributes=None)._readable_span()


def test_exporter_export(benchmark):
    benchmark(exporter.export, [span])
