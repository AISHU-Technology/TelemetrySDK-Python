#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from abc import abstractmethod, ABC
from os import linesep
from exporter.public.client import Client


class LogExporter(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def force_flush(self, timeout_millis: float = 10_000) -> bool:
        """
        强制发送缓存。
        """
        pass

    @abstractmethod
    def shutdown(self, timeout_millis: float = 30_000) -> None:
        """
        关闭实际写数据的 Client。
        """
        pass

    @abstractmethod
    def export_logs(self, logs: list[None]) -> bool:
        """
        export_logs,用来上报logs,返回上报结果。
        """
        pass


class ConsoleExporter(LogExporter):
    def __init__(
            self,
            out=sys.stdout,
            prettyprint=False,
    ):
        self.out = out
        self.formatter = lambda span: span.to_json(None)
        if prettyprint:
            self.formatter = lambda span: span.to_json()

    def export(self, spans: list[None]):
        for span in spans:
            self.out.write(self.formatter(span) + linesep)
        self.out.flush()

    def force_flush(self, timeout_millis: float = 10_000) -> bool:
        """
        没有缓存，所以不操作。
        """
        return False

    def shutdown(self, timeout_millis: float = 30_000, **kwargs) -> None:
        """
        停止写控制台。
        """
        pass

    def export_logs(self, logs: list[None]) -> bool:
        """
        写本地默认成功。
        """
        self.export(logs)
        return False
