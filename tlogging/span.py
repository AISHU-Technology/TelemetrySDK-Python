#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
import time
import random
from contextlib import contextmanager
from collections import OrderedDict
import json

from opentelemetry import trace as trace_api

from .texception import TException
from .field import Attributes, Resources, Body


_VERSION = "v1.6.1"


def check_flag(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self._Flag:
            raise TException("object has been signal")
        return func(self, *args, **kwargs)
    return wrapper


class _Span(object):

    def __init__(self, version, trace_id, span_id, severity_text, timestamp, resources, attributes, body):
        self._version = version
        self._trace_id = trace_id
        self._span_id = span_id
        self._severity_text = severity_text
        self._timestamp = timestamp
        self._resources = resources
        self._attributes = attributes
        self._body = body

    @property
    def version(self):
        return self._version

    @property
    def trace_id(self):
        return self._trace_id

    @property
    def span_id(self):
        return self._span_id

    @property
    def severity_text(self):
        return self._severity_text

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def resources(self):
        return self._resources.all_property

    @property
    def attributes(self):
        return self._attributes.all_property

    @property
    def body(self):
        return self._body.all_property

    def to_json(self, indent=4):
        my_property = OrderedDict()
        my_property["Version"] = self._version
        my_property["TraceId"] = _format_traceid(self._trace_id)
        my_property["SpanId"] = _format_spanid(self._span_id)
        my_property["SeverityText"] = self._severity_text
        my_property["Timestamp"] = self._timestamp
        if self._body:
            my_property["Body"] = self._body.all_property
        else:
            my_property["Body"] = dict()
        my_property["Resource"] = self._resources.all_property
        if self._attributes:
            my_property["Attributes"] = self._attributes.all_property
        else:
            my_property["Attributes"] = dict()
        return json.dumps(my_property, indent=indent)


class LogSpan(_Span):

    def __init__(self, processor, body, severity_text, ctx=None, attributes=None):
        self.__version = _VERSION

        self.__timestamp = self._get_time()
        self.__resources = Resources()
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Incoming parameter type is wrong: attributes")
        self.__attributes = attributes
        if not isinstance(body, Body):
            raise TException("Incoming parameter type is wrong: body")
        self.__body = body
        self.__severity_text = severity_text
        self.__processor = processor
        ctx = trace_api.get_current_span(ctx).get_span_context()
        if not ctx.trace_id:
            self.__trace_id = self._gen_trace_id()
            self.__span_id = self._gen_span_id()
        else:
            self.__trace_id = ctx.trace_id
            self.__span_id = ctx.span_id
        super(LogSpan, self).__init__(self.__version,
                                      self.__trace_id,
                                      self.__span_id,
                                      severity_text,
                                      self.__timestamp,
                                      self.__resources,
                                      attributes,
                                      body)

    # def __del__(self):
    #     if self._Flag:
    #         self.end()

    def _readable_span(self):
        return _Span(version=self.__version,
                     trace_id=self.__trace_id,
                     span_id=self.__span_id,
                     severity_text=self.__severity_text,
                     timestamp=self.__timestamp,
                     resources=self.__resources,
                     attributes=self.__attributes,
                     body=self.__body)

    # @check_flag
    def set_attributes(self, attributes):
        if not isinstance(attributes, Attributes):
            raise TException("Incoming parameter type is wrong: attributes")
        self.__attributes = attributes

    def _get_time(self):
        return int(time.time() * 1e9)

    def _gen_span_id(self):
        return random.getrandbits(64)

    def _gen_trace_id(self):
        return random.getrandbits(128)

    def end(self):
        self.__processor.on_end(self._readable_span())


class Logger(object):

    def __init__(self, processor):
        self._processor = processor

    @contextmanager
    def start_span(self, body, severity_text, attributes=None, ctx=None):
        span = None
        try:
            span = LogSpan(processor=self._processor,
                           body=body,
                           severity_text=severity_text,
                           ctx=ctx,
                           attributes=attributes)
            yield span
        except Exception as ex:
            raise TException(ex)
        finally:
            if span:
                span.end()


def _format_traceid(trace_id):
    return format(trace_id, "032x")


def _format_spanid(span_id):
    return format(span_id, "016x")
