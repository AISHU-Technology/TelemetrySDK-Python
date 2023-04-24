import json


def anyrobot_logs_from_logs(logs: "list['_Span']", indent=4) -> str:
    json_logs = json.dumps(
        obj=[
            json.loads(log.to_json())
            for log in logs
        ],
        ensure_ascii=False,
        indent=indent,
    )
    json_logs += "\n"
    return json_logs
