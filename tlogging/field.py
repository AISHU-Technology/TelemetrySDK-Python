#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket

from .texception import TException


class Resources(object):

    def __init__(self):
        self.__hostname = self._get_hostname()
        self.__telemetry_sdk_name = "Telemetry SDK"
        self.__telemetry_sdk_version = "2.0.0"
        self.__telemetry_sdk_language = "python"

    def _get_hostname(self):
        return socket.gethostname()

    @property
    def all_property(self):
        my_property = dict()
        if self.__hostname:
            my_property["HOSTNAME"] = self.__hostname
        if self.__telemetry_sdk_name:
            my_property["Telemetry.SDK.Name"] = self.__telemetry_sdk_name
        if self.__telemetry_sdk_version:
            my_property["Telemetry.SDK.Version"] = self.__telemetry_sdk_version
        if self.__telemetry_sdk_language:
            my_property["Telemetry.SDK.Language"] = self.__telemetry_sdk_language
        return my_property


class Body(object):
    def __init__(self, message, etype=None):
        if etype and not isinstance(etype, str):
            raise TException("etype should be str type")
        if not isinstance(message, str) and not etype:
            raise TException("When etype does not exist, the message should be of type str")
        self.__message = message
        self.__etype = etype

    def set_type(self, etype):
        if not isinstance(etype, str):
            raise TException("etype should be str type")
        self.__etype = etype

    def set_message(self, message):
        if not isinstance(message, str) and not self.__etype:
            raise TException("When etype does not exist, the message should be of type str")
        self.__message = message

    @property
    def all_property(self):
        my_property = dict()
        if self.__etype:
            my_property["Type"] = self.__etype
            my_property[self.__etype] = self.__message
        else:
            my_property["Message"] = self.__message

        return my_property


class Attributes(object):

    def __init__(self, message, atype):
        if atype and not isinstance(atype, str):
            raise TException("etype should be str type")
        if not atype:
            raise TException("The atype cannot be None")
        self.__message = message
        self.__atype = atype

    @property
    def all_property(self):
        my_property = dict()
        my_property["Type"] = self.__atype
        my_property[self.__atype] = self.__message

        return my_property

