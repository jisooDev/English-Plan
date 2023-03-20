from flask import Flask , render_template , redirect ,request , session  , url_for , send_file;
from dbutils.pooled_db import PooledDB ;
import pymysql ;

import os ;
from dotenv import load_dotenv ;
load_dotenv() 

from routes.admin import blueprintAdmin as admin_bp
from routes.reading import blueprintReading as reading_bp
from routes.api import blueprint as api_bp

import pyrebase

app = Flask(__name__)

pool_db = PooledDB(
    creator=pymysql, 
    maxconnections=3, 
    host=os.getenv('DB_HOST'), 
    user=os.getenv('DB_USERNAME'), 
    passwd=os.getenv('DB_PASSWORD'),
    db=os.getenv('DB_DATABASE'), 
    charset="utf8", 
    cursorclass=pymysql.cursors.DictCursor, 
    blocking=True
)

config = {
    "apiKey": "AIzaSyDExn5Hbtc_w4IT2-hUe-VT7XE7OkIT5b8",
    "authDomain": "english-plan-c76bf.firebaseapp.com",
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
    email = request.form['email']
    password = request.form['password']
    try:
        user = auth.create_user_with_email_and_password(email, password)
        print(user)
    except Exception as e:
        print(e)


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(user)
    except Exception as e:
        print(e)

@app.route("/")
def main_page():
    return render_template('main.html')

@app.route("/practice")
def practice_page():
    return render_template('practice.html')


app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(reading_bp, url_prefix='/admin')
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=70)