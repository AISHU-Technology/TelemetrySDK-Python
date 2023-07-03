import flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import SynchronousMultiSpanProcessor, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider

from exporter.ar_log.examples.multi_service_c_with_log_and_trace import db_init, mock_get_province, mock_get_city
from exporter.ar_log.log_exporter import ARLogExporter
from exporter.ar_trace.examples.multi_service_c_with_trace import get_province, get_city
from exporter.ar_trace.trace_exporter import ARTraceExporter, tracer
from exporter.config.config import Compression
from exporter.public.client import StdoutClient, HTTPClient, FileClient, ConsoleClient
from exporter.public.public import WithAnyRobotURL, WithSyncMode, WithCompression, WithTimeout, WithHeader, WithRetry
from exporter.resource.resource import set_service_info, trace_resource, log_resource
from tlogging import SamplerLogger
from tlogging.exporter import ConsoleExporter
from tlogging.tlogger import SyncLogger

app = flask.Flask(__name__)


def trace_init():
    set_service_info("YourServiceName", "2.4.2", "983d7e1d5e8cda64")
    trace_exporter = ARTraceExporter(
        FileClient("multi_service_b_with_trace.json")
    )
    # trace_exporter = ARTraceExporter(
    #     ConsoleClient()
    # )
    # trace_exporter = ARTraceExporter(
    #     StdoutClient("multi_service_b_with_trace.json")
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
    # excluded_urls填写Log上报地址，用英文逗号分隔，避免上报Log的行为被框架捕获额外生成独立的Trace。
    RequestsInstrumentor().instrument(
        excluded_urls="http://127.0.0.1/api/feed_ingester/v1/jobs/job-983d7e1d5e8cda64/events,"
                      "http://127.0.0.1/api/feed_ingester/v1/jobs/job-c9a577c302505576/events")
    FlaskInstrumentor().instrument_app(app)


def log_init():
    # 设置服务名、服务版本号、服务运行实例ID
    set_service_info("YourServiceName", "2.4.2", "983d7e1d5e8cda64")
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


@app.route("/")
def index() -> str:
    return "new page"


@app.route("/province")
def province() -> str:
    with tracer.start_as_current_span("service_province") as span:
        try:
            db_init()
            _province = get_province(3)
        except:
            _province = mock_get_province(3)
        service_logger.info(_province)
    return _province


@app.route("/city")
def city() -> str:
    with tracer.start_as_current_span("service_city") as span:
        try:
            db_init()
            _city = get_city(4)
        except:
            _city = mock_get_city(4)
        system_logger.info(_city)
    return _city


if __name__ == "__main__":
    # 在程序入口处初始化 tracer_provider 并注入正确的参数
    trace_init()
    # 在程序入口处初始化日志器并注入正确的参数
    log_init()
    # 业务代码
    app.run(port=2023, host="127.0.0.1")
