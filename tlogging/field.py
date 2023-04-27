#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import typing
from opentelemetry.sdk.resources import Attributes

from .texception import TException


class Resources(object):

    def __init__(self, attributes: dict):
        if attributes is None:
            self.__attributes = dict()
        else:
            self.__attributes = attributes

    @property
    def all_property(self):
        return self.__attributes


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
