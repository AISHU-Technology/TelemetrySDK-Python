#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from .texception import TException


class Metrics(object):

    def __init__(self):
        self.__attrubutes = dict()
        self.__labels = set()
        self.__my_property = dict()

    def set_attributes(self, k, v):
        if not isinstance(k, str):
            raise TException("k should be str type")
        if not isinstance(v, str):
            raise TException("v should be str type")
        self.__attrubutes[k] = v

    def set_other_property(self, k, v):
        if k in ["Attributes", "Labels"]:
            raise TException("k can not be Attributes or Labels")
        if not isinstance(k, str):
            raise TException("k should be str type")
        if not isinstance(v, str):
            raise TException("v should be str type")
        self.__my_property[k] = v

    def set_label(self, label):
        if not isinstance(label, str):
            raise TException("label should be str type")
        self.__labels.add(label)

    def get_all_property(self):
        if self.__attrubutes:
            self.__my_property["Attributes"] = self.__attrubutes
        if self.__attrubutes:
            self.__my_property["Labels"] = list(self.__labels)
        return self.__my_property


class Resources(object):

    def __init__(self):
        self.__hostname = self._get_hostname()
        self.__telemetry_sdk_name = "Aishu custom opentelemetry"
        self.__telemetry_sdk_version = "1.0.0"
        self.__telemetry_sdk_language = "python"

    def _get_hostname(self):
        return "localhost.localdomain"

    def get_all_property(self):
        my_property = dict()
        if self.__hostname:
            my_property["HOSTNAME"] = self.__hostname
        if self.__telemetry_sdk_name:
            my_property["telemetry.sdk.name"] = self.__telemetry_sdk_name
        if self.__telemetry_sdk_version:
            my_property["telemetry.sdk.version"] = self.__telemetry_sdk_version
        if self.__telemetry_sdk_language:
            my_property["telemetry.sdk.language"] = self.__telemetry_sdk_language
        return my_property


class Events(object):

    def __init__(self, severity, message, etype=None):
        if etype:
            if not isinstance(etype, str):
                raise TException("etype should be str type")
        if not isinstance(message, str) and not etype:
            raise TException("When mtype does not exist, the log information should be of type str")
        self.__severity = severity
        self.__message = message
        self.__timestamp = self._get_time()
        self.__etype = etype

    def get_all_property(self):
        my_property = dict()
        if self.__severity:
            my_property["SeverityText"] = self.__severity
        if self.__message:
            if self.__etype:
                my_property["type"] = self.__etype
                my_property[self.__etype] = self.__message
            else:
                my_property["message"] = self.__message
        if self.__timestamp:
            my_property["timestamp"] = self.__timestamp

        return my_property

    def _get_time(self):
        return int(time.time() * 1000)


class Attributes(object):

    def __init__(self, atype, attributes):
        if not isinstance(atype, str):
            raise TException("atype should be str type")
        self.__atype = atype
        self.__attributes = attributes

    def set_type(self, atype):
        if not isinstance(atype, str):
            raise TException("atype should be str type")
        self.__atype = atype

    def set_attributes(self, attributes):
        self.__attributes = attributes

    def get_all_property(self):
        my_property = dict()
        if self.__atype:
            my_property["type"] = self.__atype
        if self.__attributes:
            my_property[self.__atype] = self.__attributes
        return my_property


class ExternalSpans(object):
    def __init__(self):
        pass

    def get_all_property(self):
        # property = dict()
        # return property
        pass
