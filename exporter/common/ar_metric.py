import json
from dataclasses import asdict

from opentelemetry.sdk.metrics._internal.point import (
    MetricsData,
    ResourceMetrics,
    ScopeMetrics,
    Metric,
    DataT,
    Sum,
    Histogram,
    Gauge,
    NumberDataPoint,
    HistogramDataPoint,
)

from exporter.common.attribute import anyrobot_attributes_from_key_values
from exporter.common.resource import anyrobot_resource_from_resource


def anyrobot_metrics_from_resource_metrics(data: MetricsData, indent=4) -> str:
    data = json.dumps(
        obj=[
            json.loads(anyrobot_metric_from_resource_metric(resource_metrics))
            for resource_metrics in data.resource_metrics
        ],
        ensure_ascii=False,
        indent=indent,
    )
    data += "\n"
    return data


def anyrobot_metric_from_resource_metric(data: ResourceMetrics) -> str:
    return json.dumps(
        obj={
            "Resource": json.loads(anyrobot_resource_from_resource(data.resource)),
            "ScopeMetrics": [
                json.loads(anyrobot_scope_metric_from_scope_metric(scope_metrics))
                for scope_metrics in data.scope_metrics
            ],
        },
        ensure_ascii=False,
    )


def anyrobot_scope_metric_from_scope_metric(data: ScopeMetrics) -> str:
    return json.dumps(
        obj={
            "Scope": {
                "Name": data.scope.name,
                "Version": data.scope.version,
                "SchemaURL": data.scope.schema_url,
            },
            "Metrics": [
                json.loads(anyrobot_metric_from_metric(metric))
                for metric in data.metrics
            ],
        },
        ensure_ascii=False,
    )


def anyrobot_metric_from_metric(data: Metric) -> str:
    if isinstance(data.data, Sum):
        return json.dumps(
            obj={
                "Name": data.name,
                "Description": data.description or "",
                "Unit": data.unit or "",
                "Sum": json.loads(anyrobot_sum_from_sum(data.data)),
            },
            ensure_ascii=False,
        )
    if isinstance(data.data, Gauge):
        return json.dumps(
            obj={
                "Name": data.name,
                "Description": data.description or "",
                "Unit": data.unit or "",
                "Gauge": json.loads(anyrobot_gauge_from_gauge(data.data)),
            },
            ensure_ascii=False,
        )
    if isinstance(data.data, Histogram):
        return json.dumps(
            obj={
                "Name": data.name,
                "Description": data.description or "",
                "Unit": data.unit or "",
                "Histogram": json.loads(anyrobot_histogram_from_histogram(data.data)),
            },
            ensure_ascii=False,
        )


def anyrobot_sum_from_sum(data: Sum) -> str:
    return json.dumps(
        obj={
            "DataPoints": [
                json.loads(anyrobot_data_points_from_data_points(data_point))
                for data_point in data.data_points
            ],
            "Temporality": data.aggregation_temporality,
            "IsMonotonic": data.is_monotonic,
        },
        ensure_ascii=False,
    )


def anyrobot_gauge_from_gauge(data: Gauge) -> str:
    return json.dumps(
        obj={
            "DataPoints": [
                json.loads(anyrobot_data_points_from_data_points(data_point))
                for data_point in data.data_points
            ],
        },
        ensure_ascii=False,
    )


def anyrobot_histogram_from_histogram(data: Histogram) -> str:
    return json.dumps(
        obj={
            "DataPoints": [
                json.loads(
                    anyrobot_histogram_data_points_from_histogram_data_points(
                        data_point
                    )
                )
                for data_point in data.data_points
            ],
            "Temporality": data.aggregation_temporality,
        },
        ensure_ascii=False,
    )


def anyrobot_data_points_from_data_points(data: NumberDataPoint) -> str:
    if isinstance(data.value, int):
        return int_data_points(data)
    else:
        return float_data_points(data)


def int_data_points(data: NumberDataPoint) -> str:
    return json.dumps(
        obj={
            "Attributes": json.loads(
                anyrobot_attributes_from_key_values(data.attributes)
            ),
            "StartTime": data.start_time_unix_nano,
            "Time": data.time_unix_nano,
            "Int": data.value,
        },
        ensure_ascii=False,
    )


def float_data_points(data: NumberDataPoint) -> str:
    return json.dumps(
        obj={
            "Attributes": json.loads(
                anyrobot_attributes_from_key_values(data.attributes)
            ),
            "StartTime": data.start_time_unix_nano,
            "Time": data.time_unix_nano,
            "Float": data.value,
        },
        ensure_ascii=False,
    )


def anyrobot_histogram_data_points_from_histogram_data_points(
    data: HistogramDataPoint,
) -> str:
    return json.dumps(
        obj={
            "Attributes": json.loads(
                anyrobot_attributes_from_key_values(data.attributes)
            ),
            "StartTime": data.start_time_unix_nano,
            "Time": data.time_unix_nano,
            "Count": data.count,
            "Bounds": data.explicit_bounds,
            "BucketCounts": data.bucket_counts,
            "Min": data.min,
            "Max": data.max,
            "Sum": data.sum,
        },
        ensure_ascii=False,
    )
