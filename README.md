# TelemetryPython

## 安装方式
```
git clone git@gitlab.aishu.cn:anyrobot/observability/telemetrysdk/telemetry-python.git
cd telemetry-python
pip install .
```

## 使用方式
### 记录日志,不记录trace
```
from tlogging import SamplerLogger


logger = SamplerLogger()
logger.loglevel = "TraceLevel"
# 非结构化日志
logger.trace("hello, this is threading test")
# 结构化日志
logger.trace({"a": 1, "b": 2}, etype="test")
```
### 记录日志并添加attributes,不记录trace
```
from tlogging import SamplerLogger, Attributes


logger = SamplerLogger()
logger.loglevel = "TraceLevel"


attributes = attributes=Attributes({"a": "b"}, atype="test")
logger.trace("hello, this is threading test", attributes=attributes)
```
### 记录日志,也记录trace
#### 要先安装opentelemetry-sdk及相关依赖库(如opentelemetry-instrumentation-tornado、 opentelemetry-exporter-jaeger等)
#### 依赖库版本和opentelemetry-api版本一致
```
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

from tlogging import SamplerLogger, Attributes


trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "test"})
    )
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)
tracer = trace.get_tracer(__name__)
logger = SamplerLogger()
logger.loglevel = "TraceLevel"

with tracer.start_as_current_span("example-log2"):
    attributes = attributes=Attributes({"a": "b"}, atype="test")
    logger.trace("hello, this is threading test", attributes=attributes)
```
### 多线程任务记录日志,也记录trace
#### 要先安装opentelemetry-sdk及相关依赖库(如opentelemetry-instrumentation-tornado、 opentelemetry-exporter-jaeger等)
#### 依赖库版本和opentelemetry-api版本一致
```
import threading
 
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
 
from tlogging import SamplerLogger, Attributes
 
logger = SamplerLogger()
logger.loglevel = "TraceLevel"
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "test"})
    )
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)
tracer = trace.get_tracer(__name__)
prop = TraceContextTextMapPropagator()
carrier = {}
 
 
def test(num, ctx=None):
    logger.trace("hello, this is threading test" + str(num), ctx=ctx)
 
 
with tracer.start_as_current_span("example-log2"):
    logger.trace("test", attributes=Attributes({"a": "b"}, atype="test"))
    logger.trace("test1")
    logger.trace("test2")
 
logger.trace("test3")
 
with tracer.start_as_current_span("thread-log2"):
    prop.inject(carrier=carrier)
    ctx = prop.extract(carrier=carrier)
    t1 = threading.Thread(target=test, args=(1, ctx))
    t2 = threading.Thread(target=test, args=(2, ctx))
    t3 = threading.Thread(target=test, args=(3, ctx))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
```