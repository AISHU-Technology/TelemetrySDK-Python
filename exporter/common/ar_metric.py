import datetime
import json

from opentelemetry.sdk.metrics.export import (
    MetricsData,
    ResourceMetrics,
    ScopeMetrics,
    Metric,
    Sum,
    Histogram,
    Gauge,
    NumberDataPoint,
    HistogramDataPoint,
    AggregationTemporality,
)

from tzlocal import get_localzone
from exporter.common.attribute import (
    anyrobot_attributes_from_key_values,
    anyrobot_resource_from_resource,
)


def anyrobot_metrics_from_resource_metrics(metrics: MetricsData, indent=4) -> str:
    """
    转化格式统一不同语言输出数据，
    indent=4默认缩进4格，
    data += "\n"结尾换行，
    ascii=False兼容中文。
    """
    metrics = json.dumps(
        obj=[
            json.loads(anyrobot_metric_from_resource_metric(resource_metrics))
            for resource_metrics in metrics.resource_metrics
        ],
        ensure_ascii=False,
        indent=indent,
    )
    metrics += "\n"
    return metrics


def anyrobot_metric_from_resource_metric(resource_metric: ResourceMetrics) -> str:
    return json.dumps(
        obj={
            "Resource": json.loads(
                anyrobot_resource_from_resource(resource_metric.resource)
            ),
            "ScopeMetrics": [
                json.loads(anyrobot_scope_metric_from_scope_metric(scope_metrics))
                for scope_metrics in resource_metric.scope_metrics
            ],
        },
        ensure_ascii=False,
    )


def anyrobot_scope_metric_from_scope_metric(scope_metric: ScopeMetrics) -> str:
    return json.dumps(
        obj={
            "Scope": {
                "Name": scope_metric.scope.name,
                "Version": scope_metric.scope.version,
                "SchemaURL": scope_metric.scope.schema_url,
            },
            "Metrics": [
                json.loads(anyrobot_metric_from_metric(metric))
                for metric in scope_metric.metrics
            ],
        },
        ensure_ascii=False,
    )


def anyrobot_metric_from_metric(metric: Metric) -> str:
    """
    自定义 Metrics，改造了Data->Gauge/Sum/Histogram。
    """
    if isinstance(metric.data, Sum):
        return json.dumps(
            obj={
                "Name": metric.name,
                "Description": metric.description or "",
                "Unit": metric.unit or "",
                "Sum": json.loads(anyrobot_sum_from_sum(metric.data)),
            },
            ensure_ascii=False,
        )
    if isinstance(metric.data, Gauge):
        return json.dumps(
            obj={
                "Name": metric.name,
                "Description": metric.description or "",
                "Unit": metric.unit or "",
                "Gauge": json.loads(anyrobot_gauge_from_gauge(metric.data)),
            },
            ensure_ascii=False,
        )
    if isinstance(metric.data, Histogram):
        return json.dumps(
            obj={
                "Name": metric.name,
                "Description": metric.description or "",
                "Unit": metric.unit or "",
                "Histogram": json.loads(anyrobot_histogram_from_histogram(metric.data)),
            },
            ensure_ascii=False,
        )


def anyrobot_sum_from_sum(sum_: Sum) -> str:
    return json.dumps(
        obj={
            "DataPoints": [
                json.loads(anyrobot_data_point_from_data_point(data_point))
                for data_point in sum_.data_points
            ],
            "Temporality": anyrobot_temporality_from_temporality(
                sum_.aggregation_temporality
            ),
            "IsMonotonic": sum_.is_monotonic,
        },
        ensure_ascii=False,
    )


def anyrobot_gauge_from_gauge(gauge: Gauge) -> str:
    return json.dumps(
        obj={
            "DataPoints": [
                json.loads(anyrobot_data_point_from_data_point(data_point))
                for data_point in gauge.data_points
            ],
        },
        ensure_ascii=False,
    )


def anyrobot_histogram_from_histogram(histogram: Histogram) -> str:
    return json.dumps(
        obj={
            "DataPoints": [
                json.loads(
                    anyrobot_histogram_data_point_from_histogram_data_point(data_point)
                )
                for data_point in histogram.data_points
            ],
            "Temporality": anyrobot_temporality_from_temporality(
                histogram.aggregation_temporality
            ),
        },
        ensure_ascii=False,
    )


def anyrobot_data_point_from_data_point(data_point: NumberDataPoint) -> str:
    """
    自定义 DataPoint，改造了Value->Int/Float
    """
    if isinstance(data_point.value, int):
        return int_data_point(data_point)
    else:
        return float_data_point(data_point)


def int_data_point(data_point: NumberDataPoint) -> str:
    return json.dumps(
        obj={
            "Attributes": json.loads(
                anyrobot_attributes_from_key_values(data_point.attributes)
            ),
            "StartTime": anyrobot_rfc3339_nano_from_unix_nano(
                data_point.start_time_unix_nano
            ),
            "Time": anyrobot_rfc3339_nano_from_unix_nano(data_point.time_unix_nano),
            "Int": data_point.value,
        },
        ensure_ascii=False,
    )


def float_data_point(data_point: NumberDataPoint) -> str:
    return json.dumps(
        obj={
            "Attributes": json.loads(
                anyrobot_attributes_from_key_values(data_point.attributes)
            ),
            "StartTime": anyrobot_rfc3339_nano_from_unix_nano(
                data_point.start_time_unix_nano
            ),
            "Time": anyrobot_rfc3339_nano_from_unix_nano(data_point.time_unix_nano),
            "Float": data_point.value,
        },
        ensure_ascii=False,
    )


def anyrobot_histogram_data_point_from_histogram_data_point(
    histogram_data_point: HistogramDataPoint,
) -> str:
    return json.dumps(
        obj={
            "Attributes": json.loads(
                anyrobot_attributes_from_key_values(histogram_data_point.attributes)
            ),
            "StartTime": anyrobot_rfc3339_nano_from_unix_nano(
                histogram_data_point.start_time_unix_nano
            ),
            "Time": anyrobot_rfc3339_nano_from_unix_nano(
                histogram_data_point.time_unix_nano
            ),
            "Count": histogram_data_point.count,
            "Bounds": histogram_data_point.explicit_bounds,
            "BucketCounts": histogram_data_point.bucket_counts,
            "Min": histogram_data_point.min,
            "Max": histogram_data_point.max,
            "Sum": histogram_data_point.sum,
        },
        ensure_ascii=False,
    )


def anyrobot_temporality_from_temporality(temporality: AggregationTemporality) -> str:
    match temporality:
        case 1:
            return "DeltaTemporality"
        case 2:
            return "CumulativeTemporality"
        case _:
            return "undefinedTemporality"


def anyrobot_rfc3339_nano_from_unix_nano(unix_nano: int) -> str:
    """
    需要的timestamp是float类型，
    传入的unix_nano是int类型。
    """
    unix_nano = str(unix_nano)
    timestamp = float(unix_nano[:10]) + float("0." + unix_nano[10:])
    rfc3339_nano = datetime.datetime.fromtimestamp(
        timestamp, get_localzone()
    ).isoformat("T")
    result = str(rfc3339_nano)
    return result
