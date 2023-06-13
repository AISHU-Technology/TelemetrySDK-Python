#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
import time
import random
from contextlib import contextmanager
from collections import OrderedDict
import json
from os import linesep
from opentelemetry import trace as trace_api
from opentelemetry.trace import format_trace_id, format_span_id
from exporter.common.ar_metric import anyrobot_rfc3339_nano_from_unix_nano
from .processor import Processor
from .texception import TException
from .field import Attributes, Resources, Body


def check_flag(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self._Flag:
            raise TException("object has been signal")
        return func(self, *args, **kwargs)

    return wrapper


class _Span(object):

    def __init__(self, trace_id, span_id, severity_text, timestamp, resources: Resources,
                 attributes: Attributes, body: Body):
        self._link = {"TraceId": trace_id, "SpanId": span_id}
        self._timestamp = timestamp
        self._severity_text = severity_text
        self._body = body
        self._attributes = attributes
        self._resources = resources

    @property
    def link(self):
        return self._link

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def severity_text(self):
        return self._severity_text

    @property
    def body(self):
        return self._body.all_property

    @property
    def attributes(self):
        return self._attributes.all_property

    @property
    def resources(self):
        return self._resources.all_property

    def to_json(self, indent=4):
        my_property = OrderedDict()
        my_property["Link"] = self._link
        my_property["Timestamp"] = self._timestamp
        my_property["SeverityText"] = self._severity_text
        if self._body:
            my_property["Body"] = self._body.all_property
        else:
            my_property["Body"] = dict()
        if self._attributes:
            my_property["Attributes"] = self._attributes.all_property
        else:
            my_property["Attributes"] = dict()
        if self._resources:
            my_property["Resource"] = self._resources.all_property
        else:
            my_property["Resource"] = Resources(None).all_property
        return json.dumps(my_property, indent=indent, ensure_ascii=False) + linesep


class LogSpan(_Span):

    def __init__(self, processor, body: Body, severity_text, ctx=None, attributes: Attributes = None,
                 resources: Resources = None):
        self.__processor = processor
        ctx = trace_api.get_current_span(ctx).get_span_context()
        if not ctx.trace_id:
            self.__trace_id = format_trace_id(0)
            self.__span_id = format_span_id(0)
        else:
            self.__trace_id = format_span_id(ctx.trace_id)
            self.__span_id = format_span_id(ctx.span_id)
        self.__timestamp = self._get_time()
        self.__severity_text = severity_text
        if not isinstance(body, Body):
            raise TException("Incoming parameter type is wrong: body")
        self.__body = body
        if attributes and not isinstance(attributes, Attributes):
            raise TException("Incoming parameter type is wrong: attributes")
        self.__attributes = attributes
        if resources and not isinstance(resources, Resources):
            raise TException("Incoming parameter type is wrong: resources")
        self.__resources = resources

        super(LogSpan, self).__init__(
            self.__trace_id,
            self.__span_id,
            severity_text,
            self.__timestamp,
            self.__resources,
            attributes,
            body)

    def _readable_span(self):
        return _Span(trace_id=self.__trace_id,
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
        return anyrobot_rfc3339_nano_from_unix_nano(time.time_ns())
        # return int(time.time() * 1e9)

    def end(self):
        self.__processor.on_end(self._readable_span())


class Logger(object):

    def __init__(self, processor: Processor, resource: Resources):
        self._processor = processor
        self._resources = resource

    @contextmanager
    def start_span(self, body, severity_text, ctx=None, attributes=None):
        span = None
        try:
            span = LogSpan(
                body=body,
                severity_text=severity_text,
                ctx=ctx,
                attributes=attributes,
                resources=self._resources,
                processor=self._processor)
            yield span
        except Exception as ex:
            raise TException(ex)
        finally:
            if span:
                span.end()

    # self, processor, body, severity_text, ctx=None, attributes=None
    def sync_log(self, body, severity_text, attributes=None, ctx=None) -> "list['_Span']":
        span = LogSpan(processor=self._processor,
                       body=body,
                       severity_text=severity_text,
                       ctx=ctx,
                       attributes=attributes,
                       resources=self._resources)
        return [span]
