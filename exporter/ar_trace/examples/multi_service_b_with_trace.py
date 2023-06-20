import flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import SynchronousMultiSpanProcessor, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider

from exporter.ar_trace.examples.multi_service_c_with_trace import get_province, get_city
from exporter.ar_trace.trace_exporter import ARTraceExporter, tracer
from exporter.public.client import StdoutClient, HTTPClient, ConsoleClient, FileClient
from exporter.public.public import WithAnyRobotURL
from exporter.resource.resource import set_service_info, trace_resource

app = flask.Flask(__name__)


def trace_init():
    set_service_info("YourServiceName", "2.4.1", "983d7e1d5e8cda64")
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
        span_processor=BatchSpanProcessor(span_exporter=trace_exporter, schedule_delay_millis=2000,
                                          max_queue_size=10000, max_export_batch_size=400
                                          ))
    trace_provider = TracerProvider(resource=trace_resource(), active_span_processor=trace_processor)
    set_tracer_provider(tracer_provider=trace_provider)
    RequestsInstrumentor().instrument()
    FlaskInstrumentor().instrument_app(app)


@app.route("/")
def index() -> str:
    return "new page"


@app.route("/province")
def province() -> str:
    with tracer.start_as_current_span("service_province") as span:
        _province = get_province(3)
    return _province


@app.route("/city")
def city() -> str:
    with tracer.start_as_current_span("service_city") as span:
        _city = get_city(4)
    return _city


if __name__ == "__main__":
    # 在程序入口处初始化 tracer_provider 并注入正确的参数
    trace_init()
    # 业务代码
    app.run(port=2023, host="127.0.0.1")
