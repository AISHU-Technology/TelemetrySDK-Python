#!/usr/bin/env python
# -*- coding: utf-8 -*-
import atexit
import threading

from .span import Logger
from .field import Attributes, Body
from .texception import TException
from .processor import Processor
from .exporter import ConsoleExporter


_LOGLEVEL = {
    "TraceLevel": 1,
    "DebugLevel": 2,
    "InfoLevel": 3,
    "WarnLevel": 4,
    "ErrorLevel": 5,
    "FatalLevel": 6
}


class SamplerLogger(object):
    _instance_lock = threading.Lock()
    loglevel = "InfoLevel"
    exporter = ConsoleExporter()
    _span_processor = Processor(exporter)

    def __init__(self):
        self.logger = Logger(self._span_processor)
        self._atexit_handler = atexit.register(self.shutdown)

    def __new__(cls, *args, **kwargs):
        if not hasattr(SamplerLogger, "_instance"):
            with SamplerLogger._instance_lock:
                if not hasattr(SamplerLogger, "_instance"):
                    SamplerLogger._instance = object.__new__(cls)
        return SamplerLogger._instance

    def trace(self, message, attributes=None, etype=None, ctx=None):
        if _LOGLEVEL["TraceLevel"] < self._get_level():
            return
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        with self.logger.start_span(Body(message, etype), "Trace", ctx=ctx) as log_span:
            if attributes:
                log_span.set_attributes(attributes)

    def debug(self, message, attributes=None, etype=None, ctx=None):
        if _LOGLEVEL["DebugLevel"] < self._get_level():
            return
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        with self.logger.start_span(Body(message, etype), "Debug", ctx=ctx) as log_span:
            if attributes:
                log_span.set_attributes(attributes)

    def info(self, message, attributes=None, etype=None, ctx=None):
        if _LOGLEVEL["InfoLevel"] < self._get_level():
            return
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        with self.logger.start_span(Body(message, etype), "Info", ctx=ctx) as log_span:
            if attributes:
                log_span.set_attributes(attributes)

    def warn(self, message, attributes=None, etype=None, ctx=None):
        if _LOGLEVEL["WarnLevel"] < self._get_level():
            return
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        with self.logger.start_span(Body(message, etype), "Warn", ctx=ctx) as log_span:
            if attributes:
                log_span.set_attributes(attributes)

    def error(self, message, attributes=None, etype=None, ctx=None):
        if _LOGLEVEL["ErrorLevel"] < self._get_level():
            return
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        with self.logger.start_span(Body(message, etype), "Error", ctx=ctx) as log_span:
            if attributes:
                log_span.set_attributes(attributes)

    def fatal(self, message, attributes=None, etype=None, ctx=None):
        if _LOGLEVEL["FatalLevel"] < self._get_level():
            return
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        with self.logger.start_span(Body(message, etype), "Fatal", ctx=ctx) as log_span:
            if attributes:
                log_span.set_attributes(attributes)

    def _get_level(self):
        return _LOGLEVEL.get(self.loglevel, 3)

    def shutdown(self):
        self._span_processor.shutdown()
        if self._atexit_handler is not None:
            atexit.unregister(self._atexit_handler)
            self._atexit_handler = None
