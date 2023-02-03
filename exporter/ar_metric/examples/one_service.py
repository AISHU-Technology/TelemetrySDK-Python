from typing import Iterable

from opentelemetry import metrics
from opentelemetry.metrics import Observation, CallbackOptions
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
)

from exporter.config.config import Compression
from exporter.public.client import StdoutClient, HTTPClient
from exporter.ar_metric.metric_exporter import ARMetricExporter, meter
from exporter.public.public import WithAnyRobotURL, WithCompression
from exporter.resource.resource import metric_resource

reader = PeriodicExportingMetricReader(
    ARMetricExporter(StdoutClient("./AnyRobotMetric.txt"))
)
provider = MeterProvider(resource=metric_resource(), metric_readers=[reader])
metrics.set_meter_provider(provider)


def observable_gauge_func(options: CallbackOptions) -> Iterable[Observation]:
    attribute = {"用户信息": "在线用户数"}
    yield Observation(9, attribute)


def add(x: int, y: int) -> int:
    return x + y


def multiply(x: int, y: int) -> int:
    return x * y


if __name__ == "__main__":
    num = 4

    num = add(num, 7)
    meter.create_observable_gauge(
        "gauge", [observable_gauge_func], "dimension", " a simple gauge"
    )

    num = add(num, 7)
    attributes = {"用户信息": "当前用户数"}
    histogram = meter.create_histogram(
        "histogram", "dimension", "a histogram with custom buckets and name"
    )
    histogram.record(num, attributes)
    num = multiply(num, 7)
    histogram.record(num, attributes)

    num = multiply(num, 2)
    attributes = {"用户信息": "用户数日活"}
    counter = meter.create_counter("sum", "dimension", "a simple counter")
    counter.add(num, attributes)
    counter.add(num, attributes)
