import os
from arpylibs import langlib
from utils.db import db_ut_base
from utils import global_info


def install_package():
    # 安装依赖
    os.system(
        'pip3 config set global.index-url http://repository.aishu.cn:8081/repository/pypi/simple')
    os.system('pip3 config set install.trusted-host repository.aishu.cn')
    # 安装单元测试依赖
    os.system('pip3 install pytest pytest-cov  pytest-xdist  pytest-asyncio  pytest-mock')


def process_coverage_report(server_name):
    """
    修改coverage.xml（补全filename的绝对路径）
    @param server_name: 微服务名(gitlab上主代码目录名，dbio为dbio_manager)
    @return:
    """
    with open("coverage.xml", "r") as f:  # 打开文件
        data = f.read()  # 读取文件
    with open("coverage.xml", "w") as f:  # 修改文件
        new_data = data.replace(r'filename="', r'filename="%s/' % server_name)
        f.write(new_data)


if __name__ == '__main__':
    # 初始化国际化语言
    langlib.init_language()
    # 安装必要依赖
    install_package()
    import pytest

    """
     -n 3  指定3个进程并发运行测试用例
     "-s"  short
    """
    print('初始化单元测试数据库中...')
    # 初始化ut数据库
    db_ut_base.init_ut_database()
    print('当前使用的是单元测试专用数据库:', global_info.DB_NAME)

    # 运行所有单元测试用例 提交前保证以下代码未被注释掉
    pytest.main(["-s", "-v",
                 "--cov=./",
                 "--cov-report=xml",

                 "unitest/ut_modules"])
    # # 处理xml报告
    process_coverage_report(server_name='alert_manager')
    # 清除ut数据库数据
    db_ut_base.clear_ut_database()
