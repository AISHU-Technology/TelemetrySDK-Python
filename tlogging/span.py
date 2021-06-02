#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
import time
import threading

from .texception import TException
from .field import Metrics, Attributes, ExternalSpans, Resources, Events


def check_flag(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self._Flag:
            raise TException("object has been signal")
        return func(self, *args, **kwargs)
    return wrapper


class InternalSpan(object):
    _Flag = True
    _mutex = threading.Lock()

    def __init__(self, outer_func, version=None, parent_id=None, trace_id=None, span_id=None):
        if not callable(outer_func):
            raise TException("Incoming parameter type is wrong: outer_func")
        if not isinstance(trace_id, str):
            raise TException("trance_id should be str type")
        if not isinstance(parent_id, str):
            raise TException("parent_id should be str type")
        if not isinstance(span_id, str):
            raise TException("span_id should be str type")
        self.__version = version
        self.__trace_id = trace_id
        self.__span_id = span_id
        self.__parent_id = parent_id
        self.__start_time = self._get_time()
        self.__resources = Resources().get_all_property()
        self.__attributes = None
        self.__body = None
        self.__end_time = None
        self.__outer_func = outer_func

        self.__events = list()
        self.__metrics = list()
        self.__external_spans = list()

    def __del__(self):
        if self._Flag:
            self.signal()

    @check_flag
    def _set_version(self, version):
        if not isinstance(version, str):
            raise TException("version should be str type")
        self.__version = version

    @check_flag
    def _set_trance_id(self, trance_id):
        if not isinstance(trance_id, str):
            raise TException("trance_id should be str type")
        self.__trance_id = trance_id

    @check_flag
    def _get_span_id(self):
        return self.__span_id

    @check_flag
    def _get_trace_id(self):
        return self.__trace_id

    @check_flag
    def _set_span_id(self, span_id):
        if not isinstance(span_id, str):
            raise TException("trance_id should be str type")
        self.__span_id = span_id

    @check_flag
    def _set_parent_id(self, parent_id):
        if not isinstance(parent_id, str):
            raise TException("parent_id should be str type")
        self.__parent_id = parent_id

    @check_flag
    def _set_outer(self, outer_func):
        if not callable(outer_func):
            raise TException("Incoming parameter type is wrong: outer_func")
        self.__outer_func = outer_func

    @check_flag
    def _set_attributes(self, attributes):
        if not isinstance(attributes, Attributes):
            raise TException("Incoming parameter type is wrong: attributes")
        self.__attributes = attributes.get_all_property()

    @check_flag
    def _set_metrics(self, metric):
        if isinstance(metric, Metrics):
            self.__metrics.append(metric.get_all_property())
        else:
            raise TException("Incoming parameter type is wrong: metric")

    @check_flag
    def _set_events(self, event):
        if isinstance(event, Events):
            self.__events.append(event.get_all_property())
        else:
            raise TException("Incoming parameter type is wrong: event")

    @check_flag
    def _set_external_spans(self, external_span):
        if isinstance(external_span, ExternalSpans):
            self.__external_spans.append(external_span)
        else:
            raise TException("Incoming parameter type is wrong: external_span")

    @check_flag
    def signal(self):
        self._init_body()
        self._set_end()
        my_property = dict()
        if self.__version:
            my_property["Version"] = self.__version
        if self.__trace_id:
            my_property["TraceId"] = self.__trace_id
        if self.__span_id:
            my_property["SpanId"] = self.__span_id
        if self.__parent_id:
            my_property["ParentId"] = self.__parent_id
        if self.__start_time:
            my_property["StartTime"] = self.__start_time
        if self.__end_time:
            my_property["EndTime"] = self.__end_time
        if self.__body:
            my_property["Body"] = self.__body
        if self.__resources:
            my_property["Resource"] = self.__resources
        if self.__attributes:
            my_property["Attributes"] = self.__attributes

        with self._mutex:
            self._Flag = False
            try:
                self.__outer_func(my_property)
            except Exception as e:
                self._Flag = True
                raise TException(e.message)

    def _init_body(self):
        self.__body = dict()
        if self.__events:
            self.__body["Events"] = self.__events
        if self.__external_spans:
            self.__body["ExternalSpans"] = self.__external_spans
        if self.__metrics:
            self.__body["Metrics"] = self.__metrics

    def _set_end(self):
        self.__end_time = self._get_time()

    def _get_time(self):
        return int(time.time() * 1000)
