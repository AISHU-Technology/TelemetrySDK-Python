import sys

import pymysql

db = pymysql.connect(host="localhost", user="root", password="root", database="example", charset="utf8")
cursor = db.cursor()


def get_province(province_id: int) -> str:
    query = "select * from address where id = %d" % province_id
    cursor.execute(query)
    result = cursor.fetchone()
    return result[1]


def get_city(city_id: int) -> str:
    query = "select * from address where id = %d" % city_id
    cursor.execute(query)
    result = cursor.fetchone()
    return result[1]


if __name__ == "__main__":
    print(get_province(3))
    print(get_province(4))
    sys.stdout.flush()
