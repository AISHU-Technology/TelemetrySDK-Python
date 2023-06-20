### 对SDK使用者说明

文档请移步AnyRobot Eyes_Docs查看

[Trace文档链接](https://devops.aishu.cn/AISHUDevOps/AnyRobot/_git/Eyes_Docs?version=GBdevelop&_a=preview&path=%2F%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7%E5%BC%80%E5%8F%91%E8%80%85%E6%8C%87%E5%8D%97%2FTelemetrySDK%E5%BC%80%E5%8F%91%E8%80%85%E6%8C%87%E5%8D%97%2FTrace%2FPython%2FREADME.md&_a=preview)

[Log文档链接](https://devops.aishu.cn/AISHUDevOps/AnyRobot/_git/Eyes_Docs?version=GBdevelop&_a=preview&path=%2F%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7%E5%BC%80%E5%8F%91%E8%80%85%E6%8C%87%E5%8D%97%2FTelemetrySDK%E5%BC%80%E5%8F%91%E8%80%85%E6%8C%87%E5%8D%97%2FLog%2FPython%2FREADME.md&_a=preview)

[Metric文档链接](https://devops.aishu.cn/AISHUDevOps/AnyRobot/_git/Eyes_Docs?version=GBdevelop&path=%2F%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7%E5%BC%80%E5%8F%91%E8%80%85%E6%8C%87%E5%8D%97%2FTelemetrySDK%E5%BC%80%E5%8F%91%E8%80%85%E6%8C%87%E5%8D%97%2FMetric%2FPython%2FREADME.md&_a=preview)

[Event文档链接](https://devops.aishu.cn/AISHUDevOps/AnyRobot/_git/Eyes_Docs?version=GBdevelop&_a=preview&path=%2F%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7%E5%BC%80%E5%8F%91%E8%80%85%E6%8C%87%E5%8D%97%2FTelemetrySDK%E5%BC%80%E5%8F%91%E8%80%85%E6%8C%87%E5%8D%97%2FEvent%2FPython%2FREADME.md&_a=preview)

### 对SDK开发说明

#### 项目介绍

SDK提供四种可观测性数据的生产和上报，分别是Trace、Log、Metric、Event。其中Trace、Metric使用OpenTelemetry提供的SDK生产数据，Log、Event使用自研的SDK生产数据。这4种可观测性数据都使用自研的SDK上报到AnyRobot分析。

exporter目录下分别有ar_trace、ar_log、ar_metric、ar_event目录对应上报数据，以及各含子目录examples提供示例代码给SDK使用者参考。

tlogging目录下为自研Log SDK，event（暂无）目录下为为自研Event SDK。unitest目录包含单元测试和性能测试文件。

.coveragerc文件用于配置代码覆盖率检测排除哪些文件。azure-pipelines.yml文件用于非容器化构建代码检查和代码分析。

pytest_requirements.txt文件描述运行测试的依赖。requirements.txt文件描述引入SDK的依赖。

setup.py文件用于SDK构建初始化。ut_run.py文件用于运行测试代码。

#### 项目维护

[Confluence]https://confluence.aishu.cn/pages/viewpage.action?pageId=160887915

[Confluence]https://confluence.aishu.cn/display/ANYROBOT/4.+TelemetrySDK-Python

[DevOps]https://devops.aishu.cn/AISHUDevOps/ONE-Architecture/_git/TelemetrySDK-Python

[Eyes_Docs]https://devops.aishu.cn/AISHUDevOps/AnyRobot/_git/Eyes_Docs?path=%2F可观测性开发者指南%2FTelemetrySDK开发者指南

#### 代码改动

每次提交新代码需要注意的地方：

1. 查看README.md描述是否需要修改
2. 修改exporter/version/version.py/TelemetrySDKVersion
3. 修改unitest/common/test_version/TestVersion(unittest.TestCase)
4. 查看requirements.txt和setup.py/install_requires是否需要增加
5. 本地运行python ut_run.py检查单元测试是否通过
6. Eyes_Docs拉取和项目相同分支并修改对应描述
7. 提交合并主线拉取请求，和项目负责人联系审批