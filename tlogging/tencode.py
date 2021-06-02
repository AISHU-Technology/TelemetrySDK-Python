#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys

from .texception import TException


class Encoder(object):

    _OTYPE = ("json",)

    def __init__(self, encoder=None):
        if encoder and encoder not in self._OTYPE:
            raise TException("Unsupported output type")
        if encoder == "json":
            self.__encode_func = self._encode_to_json
        else:
            self.__encode_func = self._encode_to_json

    def set_encoder(self, encoder):
        if encoder not in self._OTYPE:
            raise TException("Unsupported output type")
        if encoder == "json":
            self.__encode_func = self._encode_to_json

    def tprint(self, out_info):
        if self.__encode_func:
            out_info = self.__encode_func(out_info)
        if isinstance(out_info, str):
            sys.stdout.write(out_info)
            sys.stdout.write("\n")
        else:
            print(out_info)

    def _encode_to_json(self, data):
        try:
            data_s = json.dumps(data, ensure_ascii=False)
        except:
            raise TException("object encode to json failed")

        return data_s
