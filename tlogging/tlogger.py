#!/usr/bin/env python
# -*- coding: utf-8 -*-
import atexit
from .span import Logger
from .field import Attributes, Body, Resources
from .texception import TException
from .processor import Processor
from .exporter import ConsoleExporter, LogExporter

_LOGLEVEL = {
    "AllLevel": 0,
    "TraceLevel": 1,
    "DebugLevel": 2,
    "InfoLevel": 3,
    "WarnLevel": 4,
    "ErrorLevel": 5,
    "FatalLevel": 6,
}


class SamplerLogger(object):
    loglevel = "InfoLevel"

    def __init__(self, resource: Resources, *exporters: LogExporter):
        if not exporters:
            exporters_dict = {"ConsoleExporter": ConsoleExporter()}
        else:
            exporters_dict = dict()
            for exporter in exporters:
                exporters_dict[exporter.name()] = exporter
        self._span_processor = Processor(exporters_dict)
        self.logger = Logger(self._span_processor, resource)
        self._atexit_handler = atexit.register(self.shutdown)

    def trace(self, message, attributes=None, etype=None, ctx=None):
        if _LOGLEVEL["TraceLevel"] < self._get_level():
            return
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        with self.logger.start_span(body=Body(message, etype), severity_text="Trace", ctx=ctx, attributes=attributes):
            pass

    def debug(self, message, attributes=None, etype=None, ctx=None):
        if _LOGLEVEL["DebugLevel"] < self._get_level():
            return
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        with self.logger.start_span(body=Body(message, etype), severity_text="Debug", ctx=ctx, attributes=attributes):
            pass

    def info(self, message, attributes=None, etype=None, ctx=None):
        if _LOGLEVEL["InfoLevel"] < self._get_level():
            return
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        with self.logger.start_span(body=Body(message, etype), severity_text="Info", ctx=ctx, attributes=attributes):
            pass

    def warn(self, message, attributes=None, etype=None, ctx=None):
        if _LOGLEVEL["WarnLevel"] < self._get_level():
            return
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        with self.logger.start_span(body=Body(message, etype), severity_text="Warn", ctx=ctx, attributes=attributes):
            pass

    def error(self, message, attributes=None, etype=None, ctx=None):
        if _LOGLEVEL["ErrorLevel"] < self._get_level():
            return
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        with self.logger.start_span(body=Body(message, etype), severity_text="Error", ctx=ctx, attributes=attributes):
            pass

    def fatal(self, message, attributes=None, etype=None, ctx=None):
        if _LOGLEVEL["FatalLevel"] < self._get_level():
            return
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        with self.logger.start_span(body=Body(message, etype), severity_text="Fatal", ctx=ctx, attributes=attributes):
            pass

    def _get_level(self):
        return _LOGLEVEL.get(self.loglevel)

    def shutdown(self):
        self._span_processor.shutdown()
        if self._atexit_handler is not None:
            atexit.unregister(self._atexit_handler)
            self._atexit_handler = None


class SyncLogger(object):
    loglevel = "AllLevel"

    def __init__(self, resource: Resources, exporter: LogExporter = ConsoleExporter(prettyprint=False)):
        if not exporter:
            exporter = ConsoleExporter()
        self._exporter = exporter
        self._logger = Logger(None, resource)
        self._atexit_handler = atexit.register(self.shutdown)

    def trace(self, message, attributes=None, etype=None, ctx=None) -> bool:
        if _LOGLEVEL["TraceLevel"] < self._get_level():
            return False
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        log = self._logger.sync_log(Body(message, etype), "Trace", attributes, ctx)
        return self._exporter.export_logs(log)

    def debug(self, message, attributes=None, etype=None, ctx=None) -> bool:
        if _LOGLEVEL["DebugLevel"] < self._get_level():
            return False
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        log = self._logger.sync_log(Body(message, etype), "Debug", attributes, ctx)
        return self._exporter.export_logs(log)

    def info(self, message, attributes=None, etype=None, ctx=None) -> bool:
        if _LOGLEVEL["InfoLevel"] < self._get_level():
            return False
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        log = self._logger.sync_log(Body(message, etype), "Info", attributes, ctx)
        return self._exporter.export_logs(log)

    def warn(self, message, attributes=None, etype=None, ctx=None) -> bool:
        if _LOGLEVEL["WarnLevel"] < self._get_level():
            return False
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        log = self._logger.sync_log(Body(message, etype), "Warn", attributes, ctx)
        return self._exporter.export_logs(log)

    def error(self, message, attributes=None, etype=None, ctx=None) -> bool:
        if _LOGLEVEL["ErrorLevel"] < self._get_level():
            return False
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        log = self._logger.sync_log(Body(message, etype), "Error", attributes, ctx)
        return self._exporter.export_logs(log)

    def fatal(self, message, attributes=None, etype=None, ctx=None) -> bool:
        if _LOGLEVEL["FatalLevel"] < self._get_level():
            return False
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Object is not of type Attributes")
        log = self._logger.sync_log(Body(message, etype), "Fatal", attributes, ctx)
        return self._exporter.export_logs(log)

    def _get_level(self):
        return _LOGLEVEL.get(self.loglevel)

    def shutdown(self):
        self._exporter.shutdown()
