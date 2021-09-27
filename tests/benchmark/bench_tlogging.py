#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys

from tlogging import SamplerLogger
from tlogging.exporter import ConsoleExporter
from tlogging.processor import Processor
from tlogging.span import LogSpan
from tlogging.field import Body

_VSESION = "v1.6.1"
NULL = '/dev/null'
logger = SamplerLogger()
logger.loglevel = "AllLevel"
span_mess = {
            "name": "thread test3",
            "context": {
                "trace_id": "0xdd59c2fbababb12291e3b161d105a6ce",
                "span_id": "0xb013695bb644197a",
                "trace_state": "[]"
            },
            "kind": "SpanKind.INTERNAL",
            "parent_id": "0x9944449c30965edd",
            "start_time": "2021-09-01T00:59:51.947103Z",
            "end_time": "2021-09-01T00:59:51.991947Z",
            "status": {
                "status_code": "UNSET"
            },
            "attributes": {
                "http.method": "GET",
                "http.server_name": "127.0.0.1",
                "http.scheme": "http",
                "net.host.port": 8082,
                "http.host": "127.0.0.1:8082",
                "http.target": "/index",
                "net.peer.ip": "127.0.0.1",
                "http.user_agent": "curl/7.29.0",
                "net.peer.port": 35062,
                "http.flavor": "1.1",
                "http.route": "/index",
                "http.status_code": 200
            },
            "events": [
                {
                    "name": "start request",
                    "timestamp": "2021-09-01T00:59:51.947382Z",
                    "attributes": {
                        "item.id": "ttstst",
                        "queue.id": 213123,
                        "queue.length": 4444
                    }
                },
                {
                    "name": "start request 1",
                    "timestamp": "2021-09-01T00:59:51.947422Z",
                    "attributes": {
                        "item.id": "ttstst",
                        "queue.id": 213123,
                        "queue.length": 4444
                    }
                },
                {
                    "name": "start request 2",
                    "timestamp": "2021-09-01T00:59:51.947469Z",
                    "attributes": {
                        "item.id": "ttstst",
                        "queue.id": 213123,
                        "queue.length": 4444
                    }
                },
                {
                    "name": "end request",
                    "timestamp": "2021-09-01T00:59:51.991790Z",
                    "attributes": {}
                }
            ],
            "links": [
                {
                    "context": {
                        "trace_id": "0xdd59c2fbababb12291e3b161d105a6ce",
                        "span_id": "0x9944449c30965edd",
                        "trace_state": "[]"
                    },
                    "attributes": {}
                }
            ],
            "resource": {
                "telemetry.sdk.language": "python",
                "telemetry.sdk.name": "opentelemetry",
                "telemetry.sdk.version": "1.5.0",
                "service.name": "flask-service"
            }
        }

exporter = ConsoleExporter()
_span_processor = Processor(exporter)
span = LogSpan(_span_processor, Body("test"), "test", ctx=None, attributes=None)._readable_span()


def test_add_logger_info_with_stdout(benchmark):
    benchmark(logger.info, "test")


def test_add_logger_info_without_stdout(benchmark):

    stdout = sys.stdout
    f = open('nul', 'w')
    if sys.platform.startswith("linux"):
        f = open(NULL, 'w')
    sys.stdout = f
    benchmark(logger.info, "test")
    sys.stdout = stdout


def test_sys_stdout(benchmark):
    mess = json.dumps(span_mess)
    benchmark(sys.stdout.write, mess)


def test_json_dumps(benchmark):
    benchmark(json.dumps, span_mess)


def test_span_tojson(benchmark):
    benchmark(span.to_json)


def test_json_stdout(benchmark):
    benchmark(test)


def test():
    sys.stdout.write(json.dumps(span_mess))
    sys.stdout.flush()
