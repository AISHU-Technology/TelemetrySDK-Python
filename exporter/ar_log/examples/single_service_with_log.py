from exporter.config.config import Compression
from tlogging import SamplerLogger, Attributes

from exporter.ar_log.log_exporter import ARLogExporter
from exporter.public.client import HTTPClient, StdoutClient, FileClient
from exporter.public.public import WithAnyRobotURL, WithSyncMode, WithCompression, WithTimeout, WithHeader, WithRetry
from exporter.resource.resource import log_resource, set_service_info
from tlogging.exporter import ConsoleExporter
from tlogging.tlogger import SyncLogger


def log_init():
    # 设置服务名、服务版本号、服务运行实例ID
    set_service_info("YourServiceName", "2.4.2", "983d7e1d5e8cda64")
    # 初始化系统日志器，系统日志在控制台输出，并且异步模式上报数据到数据接收器。
    global system_logger
    system_logger = SamplerLogger(log_resource(), ConsoleExporter(), ARLogExporter(
        HTTPClient(WithAnyRobotURL("http://127.0.0.1/api/feed_ingester/v1/jobs/job-983d7e1d5e8cda64/events"))))

    # 初始化业务日志器，业务日志同步模式上报数据到数据接收器。
    # ！注意配置这个参数WithSyncMode()
    global service_logger
    service_logger = SyncLogger(log_resource(), ARLogExporter(
        HTTPClient(WithAnyRobotURL("http://127.0.0.1/api/feed_ingester/v1/jobs/job-c9a577c302505576/events"),
                   WithSyncMode())))

    # 全部配置项的logger，照抄之后删掉你不需要的配置。
    global all_config_logger
    all_config_logger = SyncLogger(log_resource(), ARLogExporter(
        HTTPClient(WithAnyRobotURL("http://127.0.0.1/api/feed_ingester/v1/jobs/job-c9a577c302505576/events"),
                   WithCompression(Compression(1)),
                   WithTimeout(10),
                   WithHeader({"self-defined-header": "something"}),
                   WithRetry(5),
                   WithSyncMode())))


def add(x: int, y: int) -> int:
    # 设置属性的key中特殊字符.禁止使用
    func_attr = Attributes({"param_x": x, "param_y": y}, atype="pair")
    system_logger.warn(message="this is a info message", attributes=func_attr)
    return x + y


def multiply(x: int, y: int) -> int:
    err = service_logger.error("this is a error message")
    if err:
        print("something went wrong")
    return x * y


if __name__ == "__main__":
    # 在程序入口处初始化日志器并注入正确的参数
    log_init()
    # 业务代码
    num = add(1, 2)
    num = multiply(num, 2)
    num = add(num, 3)
    num = multiply(num, 4)
    print(num)
    """
        必须调用shutdown()否则线程无法退出，初始化了几个Logger就要shutdown几次。
    """
    system_logger.shutdown()
    service_logger.shutdown()
    all_config_logger.shutdown()
