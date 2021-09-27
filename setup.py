#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import os
import shutil


def script_path():
    """
    function: get absolute directory of the file
        in which this function defines
    usage: path = script_path()
    note: please copy the function to target script,
        don't use it like <module>.script_path()
    """
    import inspect
    this_file = inspect.getfile(inspect.currentframe())
    return os.path.abspath(os.path.dirname(this_file))


if __name__ == '__main__':
    try:
        source_path = os.path.join(script_path(), "tlogging")
        setup(name='tlogging',
              version="2.0.0",
              package_dir={"tlogging": source_path},
              packages=["tlogging"],
              zip_safe=False,
              install_requires=['opentelemetry-api==1.5.0'],
              tests_require=[
                  'allure-pytest',
                  'pytest',
                  'benchmark',
              ],
              author="Copyright (c) Aishu Software Inc.",
              description="Telemetry python SDK.",)
    finally:
        if os.path.exists('./build'):
            shutil.rmtree('./build')
        if os.path.exists('./dist'):
            shutil.rmtree('./dist')
        if os.path.exists('./tlogging.egg-info'):
            shutil.rmtree('./tlogging.egg-info')
