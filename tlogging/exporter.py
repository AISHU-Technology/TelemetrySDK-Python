#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import linesep


class ConsoleExporter(object):

    def __init__(
        self,
        out=sys.stdout,
        formatter=lambda span: span.to_json()
        + linesep,
    ):
        self.out = out
        self.formatter = formatter

    def export(self, spans):
        for span in spans:
            self.out.write(self.formatter(span))
        self.out.flush()
