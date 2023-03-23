from flask import Flask , render_template , redirect ,request , session  , url_for , send_file;
from dbutils.pooled_db import PooledDB ;
import pymysql ;
import json

import os ;
# from dotenv import load_dotenv ;
# load_dotenv() 
import query_helper as query

from routes.admin import blueprintAdmin as admin_bp
from routes.reading import blueprintReading as reading_bp
from routes.listening import blueprintListening as lintening_bp
from routes.readandwrite import blueprintReadandWrite as readandwrite_bp
from routes.talking import blueprintTalking as talking_bp
from routes.api import blueprint as api_bp

import pyrebase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'english_plan'

pool_db = PooledDB(
    creator=pymysql, 
    maxconnections=3, 
    host="43.229.76.87", 
    user="oknumber_english", 
    passwd="hubqHD66f",
    db="oknumber_english_plan", 
    charset="utf8", 
    cursorclass=pymysql.cursors.DictCursor, 
    blocking=True
)

config = {
    "apiKey": "AIzaSyDExn5Hbtc_w4IT2-hUe-VT7XE7OkIT5b8",
    "authDomain": "english-plan-c76bf.firebaseapp.com",
    "databaseURL": "https://english-plan-c76bf.firebaseapp.com",
    "projectId": "english-plan-c76bf",
    "storageBucket": "english-plan-c76bf.appspot.com",
    "messagingSenderId": "806298914847",
    "appId": "1:806298914847:web:7fe7508345e15b62a0452a",
    "measurementId": "G-7PWV72Z2QX"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data["name"]
    email = data["email"]
    password = data["password"]
    try:
        user = auth.create_user_with_email_and_password(email, password)
        user = auth.refresh(user['refreshToken'])
        user_id = user['idToken']
        try :
            query.register_user(user_id,name,user["email"])
            return json.dumps({"status" : 200})
        except Exception as e:
            print(e)
            return json.dumps({"status" : 400})
    except Exception as e:
        print(e)
        return json.dumps({"status" : 400})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        result = query.get_user_by_email(user["email"])
        if result:
            session["user_id"] = result["id"]
            session["role"] = result["role"]
            return json.dumps({"status" : 200})
        else :
            return json.dumps({"status" : 400})
    except Exception as e:
        print(e)
        return json.dumps({"status" : 400})

@app.route('/logout', methods=['GET'])
def logout():
    session["user_id"] = None
    session["role"] = None
    return render_template('main.html')

@app.route("/")
def main_page():
    return render_template('main.html')

@app.route("/practice")
def practice_page():
    return render_template('practice.html')


app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(reading_bp, url_prefix='/admin')
app.register_blueprint(lintening_bp, url_prefix='/admin')
app.register_blueprint(readandwrite_bp, url_prefix='/admin')
app.register_blueprint(talking_bp, url_prefix='/admin')
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.debug = True

    app.run(host='0.0.0.0', port=70)