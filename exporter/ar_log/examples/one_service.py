from tlogging import SamplerLogger, Attributes

from exporter.ar_log.log_exporter import ARLogExporter
from exporter.public.client import HTTPClient, StdoutClient
from exporter.public.public import WithAnyRobotURL, WithSyncMode
from exporter.resource.resource import log_resource, set_service_info
from tlogging.exporter import ConsoleExporter
from tlogging.tlogger import SyncLogger


def add_before(x: int, y: int) -> int:
    return x + y


def multiply_before(x: int, y: int) -> int:
    return x * y


def add(x: int, y: int) -> int:
    func_attr = Attributes({"param_x": x, "param_y": y}, atype="pair")
    system_logger.warn(message="this is a info message", attributes=func_attr)
    return x + y


def multiply(x: int, y: int) -> int:
    err = service_logger.error("this is a error message")
    if err:
        print("something went wrong")
    return x * y


if __name__ == "__main__":
    # 设置服务名、服务版本号、服务运行实例ID
    set_service_info("YourServiceName", "2.3.0", "983d7e1d5e8cda64")
    # 初始化系统日志器，系统日志在控制台输出，并且异步模式上报数据到数据接收器。
    system_logger = SamplerLogger(log_resource(), ConsoleExporter(), ARLogExporter(
        HTTPClient(WithAnyRobotURL("http://127.0.0.1/api/feed_ingester/v1/jobs/job-983d7e1d5e8cda64/events"))))

    # 初始化业务日志器，业务日志同步模式上报数据到数据接收器。
    # ！注意配置这个参数WithSyncMode()
    service_logger = SyncLogger(log_resource(), ARLogExporter(
        HTTPClient(WithAnyRobotURL("http://127.0.0.1/api/feed_ingester/v1/jobs/job-c9a577c302505576/events"),
                   WithSyncMode())))

    # 业务代码
    add(1, 2)
    multiply(3, 4)
