#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import threading
from os import environ

from tlogging.exporter import LogExporter

MAX_QUEUE_SIZE = "max_queue_size"
MAX_SPAN_LIST_SIZE = "max_log_sapn_size"


class Processor(object):
    def __init__(self, exporters: "dict[str, LogExporter]", max_queue_size=None, max_span_list_size=None):
        if max_queue_size is None:
            max_queue_size = int(environ.get(MAX_QUEUE_SIZE, 512))

        if max_span_list_size is None:
            max_span_list_size = int(
                environ.get(MAX_SPAN_LIST_SIZE, 49)
            )

        if max_queue_size <= 0:
            raise ValueError("max_queue_size must be a positive integer.")

        if max_span_list_size <= 0:
            raise ValueError(
                "max_log_sapn_size must be a positive integer."
            )

        if max_span_list_size > max_queue_size:
            raise ValueError(
                "max_export_batch_size must be less than or equal to max_queue_size."
            )
        self.console_exporter = exporters.pop("ConsoleExporter", None)
        self.span_exporters = exporters
        self.queue = collections.deque(
            [], max_queue_size
        )
        self.worker_thread = threading.Thread(target=self.worker, daemon=True)
        self.condition = threading.Condition(threading.Lock())
        self.max_span_list_size = max_span_list_size
        self.max_queue_size = max_queue_size
        self.done = False
        self.spans_list = [None] * self.max_span_list_size
        self.worker_thread.start()

    def on_end(self, span):
        if self.done:
            return
        if self.console_exporter:
            self.console_exporter.export_logs([span])
        if len(self.queue) >= self.max_span_list_size:
            with self.condition:
                self.condition.notify()
        self.queue.appendleft(span)

    def worker(self):
        while not self.done:
            with self.condition:
                if self.done:
                    break
                if len(self.queue) < self.max_queue_size:
                    self.condition.wait()
                    if self.done:
                        break

            self._export()
        self._drain_queue()

    def _export(self):
        idx = 0
        while idx < self.max_span_list_size and self.queue:
            self.spans_list[idx] = self.queue.pop()
            idx += 1
        try:
            for exporter in self.span_exporters.values():
                exporter.export_logs(self.spans_list[:idx])
        except Exception:
            pass
        for index in range(idx):
            self.spans_list[index] = None

    def _drain_queue(self):
        while self.queue:
            self._export()

    def shutdown(self):
        self.done = True
        with self.condition:
            self.condition.notify_all()
        self.worker_thread.join()
        for exporter in self.span_exporters.values():
            exporter.shutdown()
