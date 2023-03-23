import pymysql
import json
import time
from decimal import Decimal
from werkzeug.http import http_date

from datetime import datetime, date, timedelta

class fakefloat(float):
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return str(self._value)


def defaultencode(o):
    if isinstance(o, Decimal):
        # Subclass float with custom repr?
        return fakefloat(o)
    if isinstance(o, datetime):
        return http_date(o.utctimetuple())
    if isinstance(o, date):
        return http_date(o.timetuple())
    raise TypeError(repr(o) + " is not JSON serializable")


DB_HOST = "43.229.76.87"
DB_USER = "oknumber_english"
DB_PASSWORD = "hubqHD66f"
DB_DB = "oknumber_english_plan"

def get_connection():
    connection = pymysql.connect(**{
        'host': DB_HOST,
        'user': DB_USER,
        'password': DB_PASSWORD,
        'db': DB_DB,
        'cursorclass': pymysql.cursors.DictCursor
    })
    return connection

def register_user(uid,name,email):
    connection = get_connection()
    cursor = connection.cursor()
    sql_str = '''INSERT IGNORE INTO users (uid,name, email ,role) VALUES (
            %(uid)s, 
            %(name)s, 
            %(email)s, 
            %(role)s
        )'''

    sql_data = {
        'uid': uid,
        'name': name,
        'email': email,
        'role': "user",
    }

    cursor.execute(sql_str, sql_data)
    connection.commit()
    return True

def get_user_by_email(email):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM users WHERE email = "%s" and active = 1 LIMIT 1''' % (email))
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    return result[0]