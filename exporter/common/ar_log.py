import json


def anyrobot_logs_from_logs(logs: "list['_Span']", indent=4) -> str:
    """
    转化格式统一不同语言输出数据，
    indent=4默认缩进4格，
    data += "\n"结尾换行，
    ascii=False兼容中文。
    """
    return json.dumps(
        obj=[
            json.loads(log.to_json())
            for log in logs
        ],
        ensure_ascii=False,
        indent=indent,
    ) + "\n"
