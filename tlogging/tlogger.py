#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import os
import threading
import weakref

from .span import InternalSpan
from .field import Events, Attributes
from .texception import TException
from .tencode import Encoder


_VSESION = "AISHUV0"
_LOGLEVEL = {
    "AllLevel": 0,
    "TraceLevel": 1,
    "DebugLevel": 2,
    "InfoLevel": 3,
    "WarnLevel": 4,
    "ErrorLevel": 5,
    "FatalLevel": 6,
    "OffLevel": 7
}


class SamplerLogger(object):
    _instance_lock = threading.Lock()
    __span_set = weakref.WeakSet()

    loglevel = "InfoLevel"
    outer = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(SamplerLogger, "_instance"):
            with SamplerLogger._instance_lock:
                if not hasattr(SamplerLogger, "_instance"):
                    SamplerLogger._instance = object.__new__(cls)
        return SamplerLogger._instance

    def internal_span(self):
        if not self.outer:
            self.outer = Encoder().tprint
        inter_span = InternalSpan(version=_VSESION, parent_id="", trace_id=self.gen_id(),
                                  span_id=self.gen_id(), outer_func=self.outer)
        self.__span_set.add(inter_span)
        return inter_span

    def children_span(self, span):
        if not self.outer:
            self.outer = Encoder().tprint
        if not isinstance(span, InternalSpan):
            raise TException("Object is not of type Span")
        trance_id = span._get_trace_id()
        parent_id = span._get_span_id()
        children_span = InternalSpan(version=_VSESION, parent_id=parent_id, trace_id=trance_id,
                                     span_id=self.gen_id(), outer_func=self.outer)
        self.__span_set.add(children_span)
        return children_span

    def set_tarceid(self, tid, span):
        if not isinstance(span, InternalSpan):
            raise TException("Object is not of type Span")
        span._set_trance_id(tid)

    def set_metrics(self, metrics, span):
        if not isinstance(span, InternalSpan):
            raise TException("Object is not of type Span")
        span._set_metrics(metrics)

    def set_parentid(self, pid, span):
        if not isinstance(span, InternalSpan):
            raise TException("Object is not of type Span")
        span._set_parent_id(pid)

    def gen_id(self):
        return hashlib.sha256(os.urandom(64)).hexdigest()

    def set_attributes(self, atype, message, span):
        if not isinstance(span, InternalSpan):
            raise TException("Object is not of type Span")
        span._set_attributes(Attributes(atype, message))

    def trace(self, message, span, etype=None):
        if _LOGLEVEL["DebugLevel"] < self._get_level():
            return
        if not isinstance(span, InternalSpan):
            raise TException("Object is not of type Span")
        span._set_events(Events("Trace", message, etype))

    def debug(self, message, span, etype=None):
        if _LOGLEVEL["DebugLevel"] < self._get_level():
            return
        if not isinstance(span, InternalSpan):
            raise TException("Object is not of type Span")
        span._set_events(Events("Debug", message, etype))

    def info(self, message, span, etype=None):
        if _LOGLEVEL["DebugLevel"] < self._get_level():
            return
        if not isinstance(span, InternalSpan):
            raise TException("Object is not of type Span")
        span._set_events(Events("Info", message, etype))

    def warn(self, message, span, etype=None):
        if _LOGLEVEL["DebugLevel"] < self._get_level():
            return
        if not isinstance(span, InternalSpan):
            raise TException("Object is not of type Span")
        span._set_events(Events("Warn", message, etype))

    def error(self, message, span, etype=None):
        if _LOGLEVEL["DebugLevel"] < self._get_level():
            return
        if not isinstance(span, InternalSpan):
            raise TException("Object is not of type Span")
        span._set_events(Events("Error", message, etype))

    def fatal(self, message, span, etype=None):
        if _LOGLEVEL["DebugLevel"] < self._get_level():
            return
        if not isinstance(span, InternalSpan):
            raise TException("Object is not of type Span")
        span._set_events(Events("Fatal", message, etype))

    def close(self):
        for span in self.__span_set:
            if span._Flag:
                span.signal()
        self.__span_set = weakref.WeakSet()

    def _get_level(self):
        return _LOGLEVEL.get(self.loglevel, 3)
