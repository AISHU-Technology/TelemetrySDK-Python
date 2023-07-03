import requests
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider, SynchronousMultiSpanProcessor
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from exporter.ar_log.log_exporter import ARLogExporter
from exporter.ar_trace.trace_exporter import ARTraceExporter, tracer
from exporter.config.config import Compression
from exporter.public.client import StdoutClient, HTTPClient, FileClient, ConsoleClient
from exporter.public.public import WithAnyRobotURL, WithCompression, WithSyncMode, WithTimeout, WithHeader, WithRetry
from exporter.resource.resource import set_service_info, trace_resource, log_resource
from tlogging import SamplerLogger
from tlogging.exporter import ConsoleExporter
from tlogging.tlogger import SyncLogger


def trace_init():
    set_service_info("YourServiceName", "2.4.1", "983d7e1d5e8cda64")
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
        BatchSpanProcessor(span_exporter=trace_exporter, schedule_delay_millis=2000,
                           max_queue_size=10000, max_export_batch_size=400
                           ))
    trace_provider = TracerProvider(resource=trace_resource(), active_span_processor=trace_processor)
    set_tracer_provider(trace_provider)
    RequestsInstrumentor().instrument()


def log_init():
    # 设置服务名、服务版本号、服务运行实例ID
    set_service_info("YourServiceName", "2.4.1", "983d7e1d5e8cda64")
    # 初始化系统日志器，系统日志在控制台输出，并且异步模式上报数据到数据接收器。
    global system_logger
    system_logger = SamplerLogger(log_resource(), ConsoleExporter(), ARLogExporter(
        HTTPClient(WithAnyRobotURL("http://127.0.0.1/api/feed_ingester/v1/jobs/job-983d7e1d5e8cda64/events"))))

    # 初始化业务日志器，业务日志同步模式上报数据到数据接收器。
    # ！注意配置这个参数WithSyncMode()
    global service_logger
    service_logger = SyncLogger(log_resource(), ARLogExporter(
        HTTPClient(WithAnyRobotURL("http://127.0.0.1/api/feed_ingester/v1/jobs/job-c9a577c302505576/events"),
                   WithSyncMode())))

    # 全部配置项的logger，照抄之后删掉你不需要的配置。
    global all_config_logger
    all_config_logger = SyncLogger(log_resource(), ARLogExporter(
        HTTPClient(WithAnyRobotURL("http://127.0.0.1/api/feed_ingester/v1/jobs/job-c9a577c302505576/events"),
                   WithCompression(Compression(1)),
                   WithTimeout(10),
                   WithHeader({"self-defined-header": "something"}),
                   WithRetry(5),
                   WithSyncMode())))


def address() -> str:
    with tracer.start_as_current_span("address") as span:
        province = requests.get("http://127.0.0.1:2023/province").text
        city = requests.get("http://127.0.0.1:2023/city").text
        system_logger.info(city)
        service_logger.info(province)
    return " Address : " + province + " Province " + city + " City "


if __name__ == "__main__":
    # 在程序入口处初始化 tracer_provider 并注入正确的参数
    trace_init()
    # 在程序入口处初始化日志器并注入正确的参数
    log_init()
    # 业务代码
    print(address())
    system_logger.shutdown()
    service_logger.shutdown()
    all_config_logger.shutdown()
