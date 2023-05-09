import os
import platform
import socket

from opentelemetry.sdk.resources import Resource, Attributes
from exporter.version.version import MetricInstrumentationName, MetricInstrumentationURL, LogInstrumentationName, \
    TelemetrySDKVersion
from opentelemetry.semconv.resource import ResourceAttributes
from tlogging.field import Resources


def default_service_name() -> str:
    service_name = os.path.abspath(__file__)
    if len(service_name) <= 0:
        return "UnknownServiceName"
    return service_name


global_service_name = default_service_name()
global_service_version = "UnknownServiceVersion"
global_service_instance_id = "UnknownServiceInstanceID"


def set_service_info(name: str, version: str, instance_id: str):
    global global_service_name
    global global_service_version
    global global_service_instance_id
    global_service_name = name
    global_service_version = version
    global_service_instance_id = instance_id


def inner_attributes() -> Attributes:
    info = platform.uname()
    inner = {
        "host.ip": socket.gethostbyname(socket.gethostname()),
        ResourceAttributes.HOST_ARCH: info.machine,
        ResourceAttributes.HOST_NAME: info.node,
        ResourceAttributes.OS_TYPE: info.system,
        ResourceAttributes.OS_VERSION: info.version,
        ResourceAttributes.OS_DESCRIPTION: info.system + info.release,
        ResourceAttributes.SERVICE_NAME: global_service_name,
        ResourceAttributes.SERVICE_VERSION: global_service_version,
        ResourceAttributes.SERVICE_INSTANCE_ID: global_service_instance_id,
        ResourceAttributes.TELEMETRY_SDK_LANGUAGE: "python",
    }
    return inner


def trace_resource() -> Resource:
    attributes = inner_attributes()
    attributes[ResourceAttributes.TELEMETRY_SDK_NAME] = MetricInstrumentationName
    attributes[ResourceAttributes.TELEMETRY_SDK_VERSION] = TelemetrySDKVersion
    return Resource.create(attributes=attributes, schema_url=MetricInstrumentationURL)


def metric_resource() -> Resource:
    attributes = inner_attributes()
    attributes[ResourceAttributes.TELEMETRY_SDK_NAME] = MetricInstrumentationName
    attributes[ResourceAttributes.TELEMETRY_SDK_VERSION] = TelemetrySDKVersion
    return Resource.create(attributes=attributes, schema_url=MetricInstrumentationURL)


def log_resource() -> Resources:
    info = platform.uname()
    host = {"ip": socket.gethostbyname(socket.gethostname()), "name": info.node, "arch": info.machine}
    operating_system = {"type": info.system, "version": info.version, "description": info.system + info.release}
    sdk = {"name": LogInstrumentationName, "version": TelemetrySDKVersion, "language": "python"}
    telemetry = {"sdk": sdk}
    instance = {"id": global_service_instance_id}
    service = {"name": global_service_name, "version": global_service_version, "instance": instance}
    resource_attributes = {"host": host, "os": operating_system, "telemetry": telemetry, "service": service}
    return Resources(resource_attributes)
