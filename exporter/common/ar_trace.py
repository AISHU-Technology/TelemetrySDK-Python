import json
import typing
from opentelemetry.sdk.trace import ReadableSpan, Event
from opentelemetry.trace import SpanContext, Link, Status, StatusCode

from exporter.common.attribute import (
    anyrobot_attributes_from_key_values,
    anyrobot_resource_from_resource,
)


def anyrobot_traces_from_trace_spans(traces: typing.Sequence[ReadableSpan], indent=4) -> str:
    """
    转化格式统一不同语言输出数据，
    indent=4默认缩进4格，
    data += "\n"结尾换行，
    ascii=False兼容中文。
    """
    return json.dumps(
        obj=[json.loads(anyrobot_trace_from_trace(trace))
             for trace in traces],
        ensure_ascii=False,
        indent=indent,
    )


def anyrobot_trace_from_trace(trace: ReadableSpan) -> str:
    return json.dumps(
        obj={
            "Name": trace.name,
            "SpanContext": json.loads(anyrobot_span_context_from_context(trace.context)),
            "Parent": json.loads(anyrobot_span_context_from_context(trace.parent)),
            "SpanKind": trace.kind.value + 1,
            "StartTime": trace.start_time,
            "EndTime": trace.end_time,
            "Attributes": json.loads(anyrobot_attributes_from_key_values(trace.attributes)),
            "Links": [json.loads(anyrobot_link_from_link(link)) for link in trace.links],
            "Events": [json.loads(anyrobot_event_from_event(event)) for event in trace.events],
            "Status": json.loads(anyrobot_status_from_status(trace.status)),
            "InstrumentationScope": {
                "Name": trace.instrumentation_scope.name,
                "Version": trace.instrumentation_scope.version,
                "SchemaURL": trace.instrumentation_scope.schema_url
            },
            "Resource": json.loads(anyrobot_resource_from_resource(trace.resource)),
            "DroppedAttributes": trace.dropped_attributes,
            "DroppedEvents": trace.dropped_events,
            "DroppedLinks": trace.dropped_links,
            # ChildSpanCount 此处未实现
            "ChildSpanCount": 0,
        },
        ensure_ascii=False,
    )


def anyrobot_span_context_from_context(context: SpanContext) -> str:
    if context is None:
        return json.dumps(
            obj={
                "TraceID": "00000000000000000000000000000000",
                "SpanID": "0000000000000000",
                "TraceFlags": "00",
                "TraceState": "",
                "Remote": False,
            },
            ensure_ascii=False,
        )
    return json.dumps(
        obj={
            "TraceID": str(context.trace_id),
            "SpanID": str(context.span_id),
            "TraceFlags": "0" + str(context.trace_flags),
            "TraceState": context.trace_state.to_header(),
            "Remote": context.is_remote,
        },
        ensure_ascii=False,
    )


def anyrobot_link_from_link(link: Link) -> str:
    return json.dumps(
        obj={
            "SpanContext": json.loads(anyrobot_span_context_from_context(link.context)),
            "Attributes": json.loads(anyrobot_attributes_from_key_values(link.attributes)),
            "DroppedAttributeCount": 0,
        },
        ensure_ascii=False,
    )


def anyrobot_event_from_event(event: Event) -> str:
    return json.dumps(
        obj={
            "Name": event.name,
            "Attributes": json.loads(anyrobot_attributes_from_key_values(event.attributes)),
            "DroppedAttributeCount": 0,
            "Time": event.timestamp,
        },
        ensure_ascii=False,
    )


def anyrobot_status_from_status(status: Status) -> str:
    return json.dumps(
        obj={
            "Code": convert_status_code_to_golang(status.status_code),
            "Description": "" if status.description is None else status.description,
        },
        ensure_ascii=False,
    )


def convert_status_code_to_golang(code: StatusCode) -> int:
    print(code.name)
    if code.name == "ERROR":
        return 1
    elif code.name == "OK":
        return 2
    else:
        return 0
