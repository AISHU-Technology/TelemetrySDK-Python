from typing import Iterable, Sequence

from opentelemetry import metrics
from opentelemetry.metrics import Observation, CallbackOptions
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics._internal.aggregation import (
    ExplicitBucketHistogramAggregation,
)
from opentelemetry.sdk.metrics._internal.instrument import Histogram
from opentelemetry.sdk.metrics.view import View
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
)

from exporter.config.config import Compression
from exporter.public.client import StdoutClient, HTTPClient
from exporter.ar_metric.metric_exporter import ARMetricExporter, meter
from exporter.public.public import WithAnyRobotURL, WithCompression
from exporter.resource.resource import metric_resource, set_service_info

"""
写本地文件或者上报AR。
"""
reader = PeriodicExportingMetricReader(
    ARMetricExporter(StdoutClient("./AnyRobotMetric.json"))
    # ARMetricExporter(HTTPClient(
    #     WithAnyRobotURL("http://127.0.0.1/api/feed_ingester/v1/jobs/job-864ab9d78f6a1843/events"),
    #     WithCompression(Compression.GzipCompression),
    # ))
)

"""
如果需要自定义histogram边界值，修改传入的参数view。
"""


# boundary = [1, 2, 3]
# aggregation = ExplicitBucketHistogramAggregation(boundary)
# view = [View(instrument_type=Histogram, aggregation=aggregation)]
#
# provider = MeterProvider(
#     resource=metric_resource(), metric_readers=[reader], views=view
# )


def observable_gauge_func(options: CallbackOptions) -> Iterable[Observation]:
    attribute = {"用户信息": "在线用户数"}
    yield Observation(9, attribute)


def observable_sum_func(options: CallbackOptions) -> Iterable[Observation]:
    attribute = {"用户信息": "用户数日活"}
    yield Observation(72, attribute)


def add(x: int, y: int) -> int:
    return x + y


def multiply(x: int, y: int) -> int:
    return x * y


if __name__ == "__main__":
    set_service_info("YourServiceName", "1.0.0", "983d7e1d5e8cda64")
    provider = MeterProvider(resource=metric_resource(), metric_readers=[reader])
    metrics.set_meter_provider(provider)

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

    # counter = meter.create_observable_counter(
    #     "sum", [observable_sum_func], "dimension", "a simple counter"
    # )
