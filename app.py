from flask import Flask , render_template , redirect ,request , session  , url_for , send_file , jsonify;
from dbutils.pooled_db import PooledDB ;
import pymysql ;
import json
import stripe
from datetime import date,timedelta
from flask_caching import Cache

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
import query_helper as query

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
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
        "secret_key": "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",
        "publishable_key": "pk_live_51M1u8MGHLABh0BMzehKJKPNo3juPVvlrn3W0rYpN2datXJfu687Ef39TzmwimbIniakVLDNS3Uwosakrvb3HNdq2009Ze3LJva",
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

@app.route('/get_promotion' , methods=['POST'])
def api_get_promotion():
    data = request.json
    lang = data["lang"]
    return query.get_promotion(lang)

@app.route('/start_payment_session' , methods=['POST'])
def start_payment_session():
    data = request.json
    session["package_id"] = data["package_id"]
    print(session["user_id"])
    print(session["package_id"])
    data_log = {
        "user_id": session["user_id"],
        "package_id": session["package_id"]
    }
    query.insert_package_log(data_log)
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
       custom_text={
            "submit": {
            "message":
            str(session["user_id"]) +","+ str(session["package_id"]),
            }
        },
        mode='payment',
        success_url= request.host_url + 'success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url= request.host_url,
    )

    return jsonify({'session_id': sessions["id"]})

@app.route("/webhook", methods=['POST'])
def stripe_webhook():
    stripe_payload = request.json
    if stripe_payload["type"] == "checkout.session.completed":
        x = (stripe_payload["data"]["object"]["custom_text"]["submit"]["message"]).split(",")
        handle_checkout_session(x[0],x[1])
    return 'Success'


def handle_checkout_session(user_id , package_id):
    print("Payment was successful.")
    print(user_id)
    print(package_id)
    package = query.get_package(package_id)
    if package:
        package_id = package["id"]
        days = package["days"]
        check_package = query.get_user_package(user_id)
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
            print(data)
            query.update_user_package(data)
        else :
            start_date = date.today()
            end_date = start_date + timedelta(days=days)
            data = {
                "package_id" : package_id,
                "user_id" : user_id,
                "start_date" : start_date,
                "end_date" : end_date
            }
            print(data)
            query.insert_user_package(data)


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route('/run-atob', methods=['GET'])
def run_atob():
    try:
        res = query.get_short_answer()
        print(res)
        for x in res:
            query.update_short_answer(x["answer"],x["id"])
        return json.dumps({"status" : 200})
    except Exception as e:
        print(e)
        return json.dumps({"status" : 400})


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
            userId = result["id"]
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
    return redirect("/")

@app.route("/")
@cache.cached(timeout=1600)
def main_page():

    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str_review = '''
            SELECT * FROM review
        '''
        cursor.execute(sql_str_review)
        review = cursor.fetchall()

        sql_str_promotion = '''
           SELECT * FROM promotion_config
        '''

        cursor.execute(sql_str_promotion)
        promotions = cursor.fetchall()

        promition_EN = ''
        promition_TH = ''

        for item in promotions:
            if item['lang'] == 'EN' :
                promition_EN = item
            if item['lang'] == 'TH' :
                promition_TH = item

        sql_str_temp = '''
           SELECT * FROM temp_config
        '''

        cursor.execute(sql_str_temp)
        temp = cursor.fetchall()

        for i in temp :
            if i['type'] == 'footer' :
                footer = i
            if i['type'] == 'contact_facebook' :
                contact_facebook = i
            if i['type'] == 'contact_line' :
                contact_line = i
            if i['type'] == 'contact_email' :
                contact_email = i
            if i['type'] == 'contact_instagram' :
                contact_instagram = i

    except Exception as e :
        print(e)

    return render_template('main.html' , 
    review=review , 
    promition_EN=promition_EN , 
    promition_TH=promition_TH ,
    footer=footer ,
    contact_facebook=contact_facebook,
    contact_line=contact_line,
    contact_email=contact_email,
    contact_instagram=contact_instagram

    )

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
    app.debug = False

    app.run(host='0.0.0.0', port=3300)