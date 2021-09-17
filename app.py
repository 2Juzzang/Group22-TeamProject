from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.team22db


# 비회원 HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/login')
def loginn():
    return render_template('login.html')

@app.route('/signup')
def signupp():
    return render_template('signup.html')

# API 역할을 하는 부분
# 홈페이지(베스트셀러 주간) # 비회원 HTML 화면 보여주기
@app.route('/api/weekly', methods=['GET'])
def bestWeekly():
    weekly = list(db.weekly.find({}, {'_id': False}))
    return jsonify({'week': weekly})


@app.route('/api/monthly', methods=['GET'])
def bestmonthly():
    monthly = list(db.monthly.find({}, {'_id': False}))
    return jsonify({'month': monthly})

@app.route('/api/yearly', methods=['GET'])
def bestyearly():
    yearly = list(db.yearly.find({}, {'_id': False}))
    return jsonify({'year': yearly})


@app.route('/api/steady', methods=['GET'])
def steady():
    steady = list(db.steady.find({}, {'_id': False}))
    return jsonify({'steady': steady})

@app.route('/api/name', methods=['GET'])
def name():
    name = list(db.users.find_one({'userid':name}, {'_id': False}))
    return jsonify({'name': name})    

############아이디 중복확인 서버
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    userid_receive = request.form['userid_give'] #=> 유저네임 받기
    exists = bool(db.users.find_one({"userid": userid_receive}))
    return jsonify({'result': 'success', 'exists': exists})

############회원가입 서버
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    userid_receive = request.form['userid_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "userid": userid_receive,                               # 아이디
        "password": password_hash,                              # 비밀번호
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)