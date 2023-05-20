import pymysql
import json
import time
from decimal import Decimal
from werkzeug.http import http_date

from datetime import datetime, date, timedelta

import os ;
from dotenv import load_dotenv ;
load_dotenv() 

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


DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DB = os.getenv('DB_DATABASE')

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

def get_package(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM packages WHERE id = "%s"''' % (id))
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    return result[0]

def get_user_package(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM user_packages WHERE user_id = "%s" and active = 1 LIMIT 1''' % (user_id))
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    return result[0]

def insert_user_package(data):
    connection = get_connection()
    cursor = connection.cursor()
    sql_str = '''INSERT IGNORE INTO user_packages (user_id,package_id, start_date ,end_date) VALUES (
            %(user_id)s, 
            %(package_id)s, 
            %(start_date)s, 
            %(end_date)s
        )'''

    sql_data = {
        'user_id': data["user_id"],
        'package_id': data["package_id"],
        'start_date': data["start_date"],
        'end_date': data["end_date"],
    }

    cursor.execute(sql_str, sql_data)
    connection.commit()
    return True

def update_user_package(data):
    connection = get_connection()
    cursor = connection.cursor()
    sql_str = '''UPDATE user_packages SET package_id = %(package_id)s , start_date = %(start_date)s , end_date = %(end_date)s WHERE user_id = %(user_id)s'''

    sql_data = {
        'user_id': data["user_id"],
        'package_id': data["package_id"],
        'start_date': data["start_date"],
        'end_date': data["end_date"],
    }

    cursor.execute(sql_str, sql_data)
    connection.commit()
    return True



def handle_checkout_session(user_id , package_id):
    package = get_package(package_id)
    if package:
        package_id = package["id"]
        days = package["days"]
        check_package = get_user_package(user_id)
        if check_package:
            start_date = check_package["start_date"]
            end_date = check_package["end_date"]
            new_end_date = end_date + timedelta(days=days)
            data = {
                "package_id" : package_id,
                "user_id" : user_id,
                "start_date" : start_date,
                "end_date" : new_end_date
            }
            update_user_package(data)
        else :
            start_date = date.today()
            end_date = start_date + timedelta(days=days)
            data = {
                "package_id" : package_id,
                "user_id" : user_id,
                "start_date" : start_date,
                "end_date" : end_date
            }
            insert_user_package(data)

def insert_package_log(data):
    connection = get_connection()
    cursor = connection.cursor()
    sql_str = '''INSERT IGNORE INTO packages_log (user_id,package_id) VALUES (
            %(user_id)s, 
            %(package_id)s
        )'''

    sql_data = {
        'user_id': data["user_id"],
        'package_id': data["package_id"]
    }

    cursor.execute(sql_str, sql_data)
    connection.commit()
    return True

def get_promotion(lang):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM promotion_config WHERE lang = "%s" LIMIT 1''' % (lang))
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    return result[0]