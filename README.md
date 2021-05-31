# TelemetryPython

## 安装方式
```
git clone git@gitlab.aishu.cn:anyrobot/observability/telemetry-python.git
cd telemetry-python
pip install .
```

## 使用方式
```
import threading

from tlogging import SamplerLogger
from tlogging import Metrics


logger = SamplerLogger()   # 创建日志管理器
logger.loglevel = "AllLevel"  # 设置日志级别
span = logger.internal_span()  # 创建span
logger.set_attributes("test", {"user.id": "01", "act.type": "search topic", "user.dep": "011",
                               "act.keyword": "建筑"}, span)  # 设置attributes，attributes是用来描述sapn的信息
logger.debug("debug msg!", span)  # 写日志
logger.debug(["debug msg1!"], span, "sss") # 当日志为非str类型时，一定要传入etype，用来描述message类型
logger.debug("debug msg2!", span)
m1 = Metrics()  # 创建metrics实例
m1.set_attributes("1", "2")  # 给metrics设置attributes
m1.set_attributes("2", "3")
m1.set_label("lll")   # 给metrics设置label
logger.set_metrics(m1, span)  # 给span设置metrics
children = logger.children_span(span)  # 创建子span
logger.debug("debug msg! children0", children)  # 往子span中写入日志
children1 = logger.children_span(children)  # 创建孙span
logger.debug("debug msg! children1", children1)  # 往孙span中写入日志
 
def test():                 # 创建线程任务
    logger.debug("debug msg test!", span)
    logger.debug("debug msg test! children", children)
    logger.debug("debug msg test! children1", children1)

t1 = threading.Thread(target=test)  # 创建多线程，分别往三个span中写入日志
t2 = threading.Thread(target=test)
t1.start()
t2.start()
t1.join()
t2.join()
span.signal()  # 释放span，输出标准数据
logger.close()  # 释放所有未释放的span(已释放的span将不会再次释放)
```