# TelemetryPython

## 安装方式
```
git clone ssh://devops.aishu.cn:22/AISHUDevOps/ONE-Architecture/_git/TelemetrySDK-Python
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

## benchmark
```
============================================================================================================================ test session starts =============================================================================================================================
platform linux -- Python 3.8.0, pytest-4.6.11, py-1.11.0, pluggy-0.13.1
benchmark: 3.4.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /root/Deploy/ICT/telemetry-python3
plugins: benchmark-3.4.1, allure-pytest-2.9.45, cov-3.0.0
collected 5 items                                                                                                                                                                                                                                                            

bench_tlogging.py .....                                                                                                                                                                                                                                                [100%]


-------------------------------------------------------------------------------------------------- benchmark: 5 tests --------------------------------------------------------------------------------------------------
Name (time in ns)             Min                        Max                   Mean                  StdDev                 Median                   IQR            Outliers  OPS (Kops/s)            Rounds  Iterations
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_log_trace           385.2998 (1.0)          50,777.8605 (1.0)         483.5008 (1.0)          305.4005 (1.0)         394.1590 (1.0)          6.6939 (1.65)   11032;28901    2,068.2491 (1.0)      122595          20
test_log_debug           386.6502 (1.00)        252,907.1528 (4.98)        492.6131 (1.02)       1,696.8239 (5.56)        394.6945 (1.00)         4.0629 (1.0)     447;20887    2,029.9908 (0.98)     120480          20
test_log_warn         15,523.9832 (40.29)    21,542,055.9980 (424.24)   36,081.4025 (74.63)    189,691.7690 (621.12)   27,396.0177 (69.50)    4,150.4391 (>1000.0)   71;4080       27.7151 (0.01)      16632           1
test_log_info         15,891.8556 (41.25)        69,704.1396 (1.37)     19,754.2196 (40.86)     11,351.3508 (37.17)    16,564.9690 (42.03)    1,322.0124 (325.39)        1;3       50.6221 (0.02)         22           1
test_log_error        17,652.9866 (45.82)     3,383,598.0576 (66.64)    32,951.3099 (68.15)     62,726.4088 (205.39)   27,516.1583 (69.81)    2,485.2925 (611.70)    81;2711       30.3478 (0.01)       8953           1
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
========================================================================================================================== 5 passed in 6.28 seconds ==========================================================================================================================

```