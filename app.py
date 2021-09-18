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

#db연결 위 원격, 아래 로컬
# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.team22db

#시크릿키 선언
SECRET_KEY = 'TEAM22'

# 비회원 HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('main.html')

# 로컬에서 render_template에 methods를 사용하면 연결이 되는데
# methods를 사용하지 않을 경우 에러 로그가 발생합니다 > 10:21 git 로컬 환경 로그인 성공
# 콘솔창에서 에러가 났던 부트스트랩 관련 스크립트를 주석해주니 메서드없이 로그인이 잘 된다. > 아직
@app.route('/login' ,methods=['POST', 'GET'])
def login():
    return render_template('login.html')

#회원가입 화면
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template('signup.html')


#회원 HTMl 화면 보여주기
@app.route('/memberView')
def memberView():
    return render_template('memberView.html')


#회원 HTML 화면 보여주기
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

# 주간 베스트 뷰
@app.route('/api/weekly', methods=['GET'])
def bestWeekly():
    weekly = list(db.weekly.find({}, {'_id': False}))
    return jsonify({'week': weekly})

# 월간 베스트 뷰
@app.route('/api/monthly', methods=['GET'])
def bestmonthly():
    monthly = list(db.monthly.find({}, {'_id': False}))
    return jsonify({'month': monthly})

# 연간 베스트 뷰
@app.route('/api/yearly', methods=['GET'])
def bestyearly():
    yearly = list(db.yearly.find({}, {'_id': False}))
    return jsonify({'year': yearly})

# 스테디셀러 국내도서 뷰
@app.route('/api/steady', methods=['GET'])
def steady():
    steady = list(db.steady.find({}, {'_id': False}))
    return jsonify({'steady': steady})

# 환영 메세지 작업중
@app.route('/api/name', methods=['GET'])
def name():
    name = list(db.users.find({}, {'_id': False}))
    return jsonify({'userid': name})


#########회원가입

#아이디 중복확인 서버
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    # ajax를 통해 받아온 아이디를 변수로 지정
    userid_receive = request.form['userid_give']
    # 받아온 아이디로 db에서 찾아본 결과
    exists = bool(db.users.find_one({"userid": userid_receive}))
    # 없는 아이디라면 success를, 있는 아이디라면 exists를 보냄
    return jsonify({'result': 'success', 'exists': exists})

#회원가입 완료 서버
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    # ajax를 통해 아이디와 패스워드를 받아옴
    userid_receive = request.form['userid_give']
    password_receive = request.form['password_give']
    # 패스워드를 암호화
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # db에 저장
    doc = {
        "userid": userid_receive,
        "password": password_hash
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

##########로그인 서버

# 로그인 서버
# ajax 요청을 받음
@app.route('/sign_in')
def sign_in():
    # 아이디와 패스워드를 받아 변수로 지정
    userid_receive = request.form['userid_give']
    password_receive = request.form['password_give']
    # 패스워드는 암호화를 진행하고
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # 아이다와 암호화된 패스워드가 둘 다 일치하는 값을 찾음
    result = db.users.find_one({'userid': userid_receive, 'password': pw_hash})

    # 위 결과 None이 아니라면
    if result is not None:
        payload = {
         'id': userid_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 3)  # 로그인 3시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
    # 토큰 보냄
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면 로그인 실패 메세지
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)