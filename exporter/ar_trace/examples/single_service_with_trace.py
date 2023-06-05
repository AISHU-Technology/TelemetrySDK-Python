from opentelemetry.context import Context
from opentelemetry.sdk.trace import TracerProvider, SynchronousMultiSpanProcessor
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from exporter.ar_trace.trace_exporter import ARTraceExporter, tracer
from exporter.config.config import Compression
from exporter.public.client import StdoutClient, HTTPClient
from exporter.public.public import WithAnyRobotURL, WithCompression
from exporter.resource.resource import set_service_info, trace_resource


def trace_init():
    set_service_info("YourServiceName:Calculation", "1.0.0", "983d7e1d5e8cda64")
    trace_exporter = ARTraceExporter(
        # HTTPClient(WithAnyRobotURL("http://127.0.0.1/api/feed_ingester/v1/jobs/job-864ab9d78f6a1843/events"))
        StdoutClient("AnyRobotTrace.json")
    )
    trace_processor = SynchronousMultiSpanProcessor()
    trace_processor.add_span_processor(
        BatchSpanProcessor(span_exporter=trace_exporter, schedule_delay_millis=2000,
                           max_queue_size=10000, max_export_batch_size=400
                           ))
    trace_provider = TracerProvider(resource=trace_resource(), active_span_processor=trace_processor)
    set_tracer_provider(trace_provider)


def add(x: int, y: int) -> int:
    ctx = prop.extract(carrier=carrier)
    with tracer.start_as_current_span("add", context=ctx) as span:
        span.set_attribute("add.value", x + y)
        prop.inject(carrier=carrier)
    return x + y


def multiply(x: int, y: int) -> int:
    ctx = prop.extract(carrier=carrier)
    with tracer.start_as_current_span("multiply", context=ctx) as span:
        span.set_attribute("add.value", x * y)
        prop.inject(carrier=carrier)
    return x * y


"""
prop用于记录父节点的Context。
carrier用于存放当前节点的Context。
"""
prop = TraceContextTextMapPropagator()
carrier = {}

if __name__ == "__main__":
    # 在程序入口处初始化 tracer_provider 并注入正确的参数
    trace_init()

    # 业务代码
    num = add(1, 2)
    num = multiply(num, 2)
    num = add(num, 3)
    num = multiply(num, 4)
    print(num)
