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

#######db연결########
# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.team22db

#######시크릿키 선언#######
SECRET_KEY = 'TEAM22'

# 비회원 HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


#회원 HTMl 화면 보여주기
@app.route('/member')
def memberView():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload['id']})
        return render_template('memberView.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/memberView')
def memberView():
    return render_template('memberView.html')

# API 역할을 하는 부분
# 홈페이지(베스트셀러 주간) # 비회원 HTML 화면 보여주기
@app.route('/member')
def member():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload['id']})
        return redirect("memberView", user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

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


#########회원가입, 로그인#############
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
        "userid": userid_receive,
        "password": password_hash
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

############로그인 서버

@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    userid_receive = request.form['userid_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'userid': userid_receive, 'password': pw_hash})
    
    if result is not None:
        payload = {
         'id': userid_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 3)  # 로그인 3시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)