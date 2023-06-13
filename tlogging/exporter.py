#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from abc import abstractmethod, ABC


class LogExporter(ABC):

    @abstractmethod
    def name(self) -> str:
        """
        Exporter唯一标识。
        """
        pass

    @abstractmethod
    def shutdown(self, timeout_millis: float = 30_000) -> None:
        """
        关闭实际写数据的 Client。
        """
        pass

    @abstractmethod
    def export_logs(self, logs: "list['_Span']") -> bool:
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

    def export(self, spans: "list['_Span']"):
        for span in spans:
            self.out.write(self.formatter(span))
        self.out.flush()

    def name(self) -> str:
        """
        没有缓存，所以不操作。
        """
        return "ConsoleExporter"

    def shutdown(self, timeout_millis: float = 30_000, **kwargs) -> None:
        """
        停止写控制台。
        """
        pass

    def export_logs(self, logs: "list['_Span']") -> bool:
        """
        写本地默认成功。
        """
        self.export(logs)
        return False
