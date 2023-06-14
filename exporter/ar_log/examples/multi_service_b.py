import flask

from exporter.ar_trace.examples.multi_service_c import get_province

app = flask.Flask(__name__)


@app.route("/")
def index() -> str:
    return "new page"


@app.route("/province")
def province() -> str:
    _province = get_province(3)
    return _province


@app.route("/city")
def city() -> str:
    _city = get_province(4)
    return _city


if __name__ == "__main__":
    # 业务代码
    app.run(port=2023, host="127.0.0.1")
