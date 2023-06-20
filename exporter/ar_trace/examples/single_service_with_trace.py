from opentelemetry.context import Context
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
    set_service_info("YourServiceName", "2.4.1", "983d7e1d5e8cda64")
    trace_exporter = ARTraceExporter(
        FileClient("AnyRobotTrace.json")
    )
    # trace_exporter = ARTraceExporter(
    #     ConsoleClient()
    # )
    # trace_exporter = ARTraceExporter(
    #     StdoutClient("AnyRobotTrace.json")
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


def add(x: int, y: int) -> int:
    ctx = prop.extract(carrier=carrier)
    with tracer.start_as_current_span("add", context=ctx) as span:
        # 设置属性的key中特殊字符.禁止使用
        span.set_attribute("add_value", x + y)
        prop.inject(carrier=carrier)
    return x + y


def multiply(x: int, y: int) -> int:
    ctx = prop.extract(carrier=carrier)
    with tracer.start_as_current_span("multiply", context=ctx) as span:
        # 设置属性的key中特殊字符.禁止使用
        span.set_attribute("add_value", x * y)
        prop.inject(carrier=carrier)
    return x * y


"""
prop用于记录父节点的Context。
carrier用于存放当前节点的Context。
这两个参数的作用是把原本业务上顺序执行的函数，不存在父子关系的函数，记录在一条链路上。
如果存在父子关系，则不需要配置这两个参数。
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
