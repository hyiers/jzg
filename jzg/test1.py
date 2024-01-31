from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import uuid
import time
import hmac
import hashlib
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/pt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class person(db.Model):
    __tablename__ = 'person'
    personname = db.Column(db.String, primary_key=True)
    gender = db.Column(db.String, nullable=True)
    orgindexcode = db.Column(db.String, nullable=True)
    birthday = db.Column(db.String, nullable=True)
    phoneno = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    certificatetype = db.Column(db.String, nullable=True)
    certificateno = db.Column(db.String, nullable=True)
    jobno = db.Column(db.String, nullable=True)
    faces = db.Column(db.String, nullable=True)

with app.app_context():
    db.create_all()
    
base_url = "http://127.0.0.1:5000"
api_add_person_url = "/api/resource/v2/person/single/add"
appKey = "22932116"
appSecret = "GSCOsNc7EMA61FfjE"

def sign(key, value):
    temp = hmac.new(key.encode(), value.encode(), digestmod=hashlib.sha256)
    return base64.b64encode(temp.digest()).decode()

@app.route(api_add_person_url, methods=['POST'])
def add_person():
    x_ca_nonce = str(uuid.uuid4())
    x_ca_timestamp = str(int(round(time.time()) * 1000))
    sign_str = f"POST\n*/*\napplication/json\nx-ca-key:{appKey}\nx-ca-nonce:{x_ca_nonce}\nx-ca-timestamp:{x_ca_timestamp}\n{api_add_person_url}"
    signature = sign(appSecret, sign_str)
    
    Accept = request.headers.get('Accept')
    ContentType = request.headers.get('Content-Type')
    xcakey = request.headers.get('x-ca-key')
    xcasignatureheaders = request.headers.get('x-ca-signature-headers')
    xcasignature = request.headers.get('x-ca-signature')
    xcatimestamp = request.headers.get('x-ca-timestamp')
    xcanonce = request.headers.get('x-ca-nonce')

    


    if auth_id != "9044143925417" or auth_key != "sakvxb36":
        print("Authentication failed")
        return jsonify({"error": "Authentication failed"}), 401
    try:
        x_ca_nonce = str(uuid.uuid4())
        x_ca_timestamp = str(int(round(time.time()) * 1000))

        # 获取请求的 JSON 数据
        request_data = request.json

        # 转换请求数据为 JSON 字符串
        request_data_str = json.dumps(request_data, separators=(',', ':'))

        # 构造签名字符串
        sign_str = f"POST\n*/*\napplication/json\nx-ca-key:{appKey}\nx-ca-nonce:{x_ca_nonce}\nx-ca-timestamp:{x_ca_timestamp}\n{api_add_person_url}"

        # 生成签名
        signature = sign(appSecret, sign_str)

        # 构造请求头
        headers = {
            "Accept": "*/*",
            'Content-Type': 'application/json',
            "x-ca-key": '22932116',
            "x-ca-signature-headers": "x-ca-key,x-ca-nonce,x-ca-timestamp",
            "x-ca-signature": signature,
            "x-ca-timestamp": x_ca_timestamp,
            "x-ca-nonce": x_ca_nonce
        }

        # 发送请求
        response = requests.post(base_url + ":5001" + api_add_person_url, json=request_data, headers=headers)

        # 解析响应并返回给客户端
        
        return jsonify(name="John Doe")

    except Exception as e:
        # 处理异常
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5001)

