import json


def anyrobot_logs_from_logs(logs: list[None], indent=4) -> str:
    logs = json.dumps(
        obj=logs,
        ensure_ascii=False,
        indent=indent,
    )
    logs += "\n"
    return logs
