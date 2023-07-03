import requests
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider, SynchronousMultiSpanProcessor
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from exporter.ar_trace.trace_exporter import ARTraceExporter, tracer
from exporter.config.config import Compression
from exporter.public.client import StdoutClient, HTTPClient, FileClient, ConsoleClient
from exporter.public.public import WithAnyRobotURL, WithCompression
from exporter.resource.resource import set_service_info, trace_resource


def trace_init():
    set_service_info("YourServiceName", "2.4.2", "983d7e1d5e8cda64")
    trace_exporter = ARTraceExporter(
        FileClient("multi_service_a_with_trace.json")
    )
    # trace_exporter = ARTraceExporter(
    #     ConsoleClient()
    # )
    # trace_exporter = ARTraceExporter(
    #     StdoutClient("multi_service_a_with_trace.json")
    # )
    # trace_exporter = ARTraceExporter(
    #     HTTPClient(WithAnyRobotURL("http://127.0.0.1/api/feed_ingester/v1/jobs/job-864ab9d78f6a1843/events"))
    # )
    trace_processor = SynchronousMultiSpanProcessor()
    trace_processor.add_span_processor(
        span_processor=BatchSpanProcessor(span_exporter=trace_exporter, schedule_delay_millis=2000,
                                          max_queue_size=10000, max_export_batch_size=400
                                          ))
    trace_provider = TracerProvider(resource=trace_resource(), active_span_processor=trace_processor)
    set_tracer_provider(tracer_provider=trace_provider)
    RequestsInstrumentor().instrument()


def address() -> str:
    with tracer.start_as_current_span("address") as span:
        province = requests.get("http://127.0.0.1:2023/province").text
        city = requests.get("http://127.0.0.1:2023/city").text
    return " Address : " + province + " Province " + city + " City "


if __name__ == "__main__":
    # 在程序入口处初始化 tracer_provider 并注入正确的参数
    trace_init()
    # 业务代码
    print(address())
