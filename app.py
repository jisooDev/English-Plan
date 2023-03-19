from flask import Flask , render_template , redirect ,request , session  , url_for , send_file;
from dbutils.pooled_db import PooledDB ;
import pymysql ;

import os ;
from dotenv import load_dotenv ;
load_dotenv() 

from routes.admin import blueprint as admin_bp
from routes.api import blueprint as api_bp

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

@app.route("/")
def main_page():
    return render_template('main.html')

@app.route("/practice")
def practice_page():
    return render_template('practice.html')


app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=70)