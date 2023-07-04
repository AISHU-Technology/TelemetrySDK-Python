import pymysql

from exporter.ar_trace.trace_exporter import tracer


def db_init():
    global db, cursor
    db = pymysql.connect(host="localhost", user="root", password="root", database="example", charset="utf8")
    cursor = db.cursor()


def get_province(province_id: int) -> str:
    with tracer.start_as_current_span("db_get_province") as span:
        query = "select * from address where id = %d" % province_id
        cursor.execute(query)
        result = cursor.fetchone()
    return result[1]


def get_city(city_id: int) -> str:
    with tracer.start_as_current_span("db_get_city") as span:
        query = "select * from address where id = %d" % city_id
        cursor.execute(query)
        result = cursor.fetchone()
    return result[1]


def mock_get_province(province_id: int) -> str:
    with tracer.start_as_current_span("mock_get_province") as span:
        return "SiChuan"


def mock_get_city(city_id: int) -> str:
    with tracer.start_as_current_span("mock_get_city") as span:
        return "ChengDu"


if __name__ == "__main__":
    try:
        db_init()
        print(get_province(3))
        print(get_city(4))
    except:
        print(mock_get_province(3))
        print(mock_get_city(4))
