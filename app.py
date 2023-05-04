from flask import Flask , render_template , redirect ,request , session  , url_for , send_file , jsonify;
from dbutils.pooled_db import PooledDB ;
import pymysql ;
import json
import stripe
from datetime import date

import os ;
from dotenv import load_dotenv ;
load_dotenv() 

import query_helper as query
from routes.admin import blueprintAdmin as admin_bp
from routes.reading import blueprintReading as reading_bp
from routes.listening import blueprintListening as lintening_bp
from routes.readandwrite import blueprintReadandWrite as readandwrite_bp
from routes.talking import blueprintTalking as talking_bp
from routes.config import blueprintConfig as config_bp
from routes.api import blueprint as api_bp

import pyrebase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'english_plan'

pool_db = PooledDB(
    creator=pymysql, 
    maxconnections=3, 
    host=os.getenv('DB_HOST'), 
    user=os.getenv('DB_USERNAME'), 
    passwd=os.getenv('DB_PASSWORD'),
    db=os.getenv('DB_DATABASE'),
    # host="43.229.76.87", 
    # user="oknumber_english", 
    # passwd="hubqHD66f",
    # db="oknumber_english_plan", 
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

stripe_keys = {
        "secret_key": "sk_test_51Myfx5Fs6C8dHOiLePaJ3eeCfK4OoRCkLXIdylU7gvbc6KJCa8gJmSkVWKqNqfSJL8giPnljhah3kT3J1dkQcCxy00rTuPppNg",
        "publishable_key": "pk_test_51Myfx5Fs6C8dHOiLU9lOp1Sm5QBs129Wr57ycT4wraPdELWgo3Vy2ILQgNnjKzrNoJdeNPuveOcRMsvnkjfhJNHk00TIFyrDyx",
        "endpoint_secret": "english_plans"
}

stripe.api_key = stripe_keys["secret_key"]


@app.before_request
def check_admin():
    if request.path.startswith('/admin/') and ('role' not in session or session['role'] != 'admin'):
        return redirect('/')

@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)

@app.route('/set_session_package' , methods=['POST'])
def set_session_package():
    data = request.json
    session["package_id"] = data["package_id"]
    return "Success"

@app.route('/start_payment_session' , methods=['POST'])
def start_payment_session():
    data = request.json
    stripe.api_key = stripe_keys["secret_key"]
    sessions = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            "price_data": {
            "currency": 'usd',
            "product_data": {
            "name": data["name"],
            },
            "unit_amount": data["unit_amount"],
            },
            "quantity": 1,
        }],
        mode='payment',
        success_url= request.host_url + 'success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url= request.host_url,
    )

    return jsonify({'session_id': sessions["id"]})

@app.route("/webhook", methods=['POST'])
def stripe_webhook():
    stripe_payload = request.json
    print(stripe_payload)
    if stripe_payload["type"] == "checkout.session.completed":
        handle_checkout_session()
    return 'Success'


def handle_checkout_session():
    print("Payment was successful.")
    user_id = session["user_id"]
    package = query.get_package(session["package_id"])
    if package:
        package_id = package["id"]
        days = package["days"]
        check_package = query.get_user_package(user_id)
        if check_package:
            start_date = check_package["start_date"]
            end_date = check_package["end_date"]
            new_start_date = end_date
            new_end_date = end_date + days
            data = {
                package_id : package_id,
                user_id : user_id,
                start_date : new_start_date,
                end_date : new_end_date
            }
            update = query.update_user_package(data)
            print("update package user_id = "+ user_id +" " +update)
        else :
            start_date = date.today()
            end_date = start_date + days
            data = {
                package_id : package_id,
                user_id : user_id,
                start_date : start_date,
                end_date : end_date
            }
            insert = query.insert_user_package(data)
            print("insert package user_id = "+ user_id +" " +insert)


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data["name"]
    email = data["email"]
    password = data["password"]
    try:
        user = auth.create_user_with_email_and_password(email, password)
        user = auth.refresh(user['refreshToken'])
        user_id = user['userId']
        query.register_user(user_id,name,email)
        return json.dumps({"status" : 200})
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
            print(session["user_id"])
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

@app.route("/exam")
def practice_page():
    return render_template('practice.html')



app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(reading_bp, url_prefix='/admin')
app.register_blueprint(lintening_bp, url_prefix='/admin')
app.register_blueprint(readandwrite_bp, url_prefix='/admin')
app.register_blueprint(talking_bp, url_prefix='/admin')
app.register_blueprint(config_bp, url_prefix='/admin')
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.debug = True

    app.run(host='0.0.0.0', port=3300)