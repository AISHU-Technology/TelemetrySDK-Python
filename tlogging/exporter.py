#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import linesep


class ConsoleExporter(object):

    def __init__(
        self,
        out=sys.stdout,
        prettyprint=False,
    ):
        self.out = out
        self.formatter = lambda span: span.to_json(None)
        if prettyprint:
            self.formatter = lambda span: span.to_json()


    def export(self, spans):
        for span in spans:
            self.out.write(self.formatter(span) + linesep)
        self.out.flush()
