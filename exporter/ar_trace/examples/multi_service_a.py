import requests


def address() -> str:
    province = requests.get("http://127.0.0.1:2023/province").text
    city = requests.get("http://127.0.0.1:2023/city").text
    return " Address : " + province + " Province " + city + " City "


if __name__ == "__main__":
    # 业务代码
    print(address())
