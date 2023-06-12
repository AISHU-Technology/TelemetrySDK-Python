import pymysql

from exporter.ar_trace.trace_exporter import tracer

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


if __name__ == "__main__":
    print(get_province(3))
    print(get_province(4))
