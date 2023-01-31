from typing import Iterable

from opentelemetry import metrics
from opentelemetry.metrics import Observation, CallbackOptions
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
)

from exporter.public.client import StdoutClient, HTTPClient
from exporter.ar_metric.metric_exporter import ARMetricExporter, meter
from exporter.resource.resource import metric_resource

reader = PeriodicExportingMetricReader(
    ARMetricExporter(
        # HTTPClient(
        #     WithAnyRobotURL(
        #         # "http://127.0.0.1:8800/api/feed_ingester/v1/jobs/job-abcd4f634e80d530/events"
        #         "http://10.4.130.68:13048/api/feed_ingester/v1/jobs/Kitty1/events"
        #     ),
        #     WithCompression(Compression.NoCompression),
        # )
        StdoutClient("./AnyRobotMetric.txt")
    )
)
provider = MeterProvider(resource=metric_resource(), metric_readers=[reader])
metrics.set_meter_provider(provider)


def observable_gauge_func(options: CallbackOptions) -> Iterable[Observation]:
    attributes = {"用户信息": "用户数峰值"}
    yield Observation(9, attributes)


def add(x: int, y: int) -> int:
    attributes = {"用户信息": "在线用户数"}
    gauge = meter.create_observable_gauge(
        "gauge", [observable_gauge_func], "dimension", " a simple gauge"
    )
    attributes = {"用户信息": "用户数日活"}
    counter = meter.create_counter("sum", "dimension", "a simple counter")
    counter.add(30, attributes)
    counter.add(46, attributes)
    return x + y


def multiply(x: int, y: int) -> int:
    attributes = {"用户信息": "当前用户数"}
    histogram = meter.create_histogram(
        "histogram", "dimension", "a histogram with custom buckets and name"
    )
    histogram.record(100, attributes)
    histogram.record(300, attributes)
    return x * y


if __name__ == "__main__":
    num = 4
    num = add(num, 2)
    num = multiply(num, 7)
