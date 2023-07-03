# 代码示例说明

## 调用关系

single_service.py单独文件

## single_service.py

原始的包含同一个服务内提供加法、乘法处理函数。

## single_service_with_trace.py

改造后的同一个服务内加法、乘法函数在不是父子调用关系时，在同一条调用链上的代码埋点示例，目的是展示如何在代码中加入链路的初始化配置。

# single_service运行过程

先阅读single_service.py代码，后运行。
再阅读single_service_with_trace.py代码，后运行比较区别。查看AnyRobotTrace.json。

# 代码示例说明

## 调用关系

multi_service_a.py->multi_service_b.py->multi_service_c.py

## multi_service_a.py

原始的包含查询省份+城市的地址信息的函数。

## multi_service_b.py

使用了flask框架的服务，运行在本地。分别提供查询省份接口和查询城市接口。

## multi_service_c.py

数据库查询服务，传入省份id或城市id，返回结果。需要连接本地数据库并填充简单示例。

| id  | address  |
|:---:|:--------:|
|  1  | ShangHai |
|  2  | BeiJing  |
|  3  | SiChuan  |
|  4  | ChengDu  |

## multi_service_a_with_trace.py

改造后的模拟查询地址程序入口，目的是展示父子关系调用，如何在代码中加入链路的初始化配置以及在Python服务调用链中跨服务传播链路上下文信息。

## multi_service_b_with_trace.py

改造后的flask框架，加入了传播链路上下文信息的插件：FlaskInstrumentor、RequestsInstrumentor。

## multi_service_c_with_trace.py

改造后的数据库查询模拟。

# multi_service运行过程

1. 示例代码仅用于调试不用于生产，因此导包没有添加进requirement.txt，需要自行添加示例代码需要的依赖。
2. opentelemetry-instrumentation-requests~=0.38b0 opentelemetry-instrumentation-flask==0.38b0。
3. 准备好本地数据库用于调试，直到成功运行multi_service_c.py。
4. 启动multi_service_b.py，运行multi_service_a.py，成功获取“Address : SiChuan Province ChengDu City”。
5. 切换成运行multi_service_b_with_trace.py、multi_service_a_with_trace.py，查看控制台和本地文件。
6. StdoutClient仅用于调试，正式使用应修改为HTTPClient。




