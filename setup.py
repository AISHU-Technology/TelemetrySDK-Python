#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
import shutil

from exporter.version.version import TelemetrySDKVersion

if __name__ == '__main__':
    try:
        setup(name='TelemetrySDK-Python',
              version=TelemetrySDKVersion,
              description='包含Trace、Log、Metric的可观测性数据生产并上报到AnyRobot分析的软件包',
              long_description='原Log文档链接:tlogging/README.md;新Exporter文档链接:exporter/README.md',
              author='上海爱数信息技术股份有限公司©',
              url='https://www.aishu.cn/',
              download_ur='https://devops.aishu.cn/AISHUDevOps/ONE-Architecture/_git/TelemetrySDK-Python',
              packages=find_packages(),
              classifiers=['Development Status :: 5 - Production/Stable',
                           'Intended Audience :: Developers',
                           'Topic :: Software Development :: SDK'],
              zip_safe=False,
              install_requires=['opentelemetry-api==1.15.0'],
              tests_require=[
                  'allure-pytest',
                  'pytest',
                  'benchmark',
              ],
              python_requires='>=3.7',
              ),
    finally:
        if os.path.exists('./build'):
            shutil.rmtree('./build')
        if os.path.exists('./dist'):
            shutil.rmtree('./dist')
        if os.path.exists('./tlogging.egg-info'):
            shutil.rmtree('./tlogging.egg-info')
