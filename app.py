from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

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
# 홈페이지(베스트셀러 주간)
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
#
# @app.route('/api/yearly', methods=['GET'])
# def show_stars():
#     sample_receive = request.args.get('sample_give')
#     print(sample_receive)
#     return jsonify({'msg': 'list 연결되었습니다!'})
#
# @app.route('/api/steady', methods=['GET'])
# def show_stars():
#     sample_receive = request.args.get('sample_give')
#     print(sample_receive)
#     return jsonify({'msg': 'list 연결되었습니다!'})
#
# @app.route('/api/detail', methods=['GET'])
# def show_stars():
#     sample_receive = request.args.get('sample_give')
#     print(sample_receive)
#     return jsonify({'msg': 'list 연결되었습니다!'})
#
# @app.route('/api/favorite', methods=['GET'])
# def show_stars():
#     sample_receive = request.args.get('sample_give')
#     print(sample_receive)
#     return jsonify({'msg': 'list 연결되었습니다!'})
#
# @app.route('/api/signin', methods=['POST'])
# def like_star():
#     sample_receive = request.form['sample_give']
#     print(sample_receive)
#     return jsonify({'msg': 'like 연결되었습니다!'})
#
#
# @app.route('/api/signup', methods=['POST'])
# def like_star():
#     sample_receive = request.form['sample_give']
#     print(sample_receive)
#     return jsonify({'msg': 'like 연결되었습니다!'})
#
# @app.route('/api/heart', methods=['POST'])
# def like_star():
#     sample_receive = request.form['sample_give']
#     print(sample_receive)
#     return jsonify({'msg': 'like 연결되었습니다!'})
#
# @app.route('/api/break', methods=['POST'])
# def like_star():
#     sample_receive = request.form['sample_give']
#     print(sample_receive)
#     return jsonify({'msg': 'like 연결되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)