from flask import Flask, jsonify, request
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
    personid = db.Column(db.String, primary_key=True)
    personname = db.Column(db.String, nullable=True)
    gender = db.Column(db.String, nullable=True)
    orgindexcode = db.Column(db.String, nullable=True)
    birthday = db.Column(db.String, nullable=True)
    phoneno = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    certificatetype = db.Column(db.String, nullable=True)
    certificateno = db.Column(db.String, nullable=True)
    jobno = db.Column(db.String, nullable=True)
    faces = db.Column(db.String, nullable=True)
    facesid = db.Column(db.String, nullable=True)


with app.app_context():
    db.create_all()

base_url = "http://127.0.0.1:5000"
appSecret = "GSCOsNc7EMA61FfjE"
api_add_person_url = "/api/resource/v2/person/single/add"
x_ca_nonce = str(uuid.uuid4())
x_ca_timestamp = str(int(round(time.time()) * 1000))

def sign(key, value):
    temp = hmac.new(key.encode(), value.encode(), digestmod=hashlib.sha256)
    return base64.b64encode(temp.digest()).decode()

def simulate_api_request():
    existing_person = person.query.all()
    appKey = "22932116"
    sign_str = f"POST\n*/*\napplication/json\nx-ca-key:{appKey}\nx-ca-nonce:{x_ca_nonce}\nx-ca-timestamp:{x_ca_timestamp}\n{api_add_person_url}"  
    signature = sign(appSecret, sign_str)

    headers = {
        "Accept": "*/*",
        'Content-Type': 'application/json',
        "x-ca-key": appKey,
        "x-ca-signature-headers": "x-ca-key,x-ca-nonce,x-ca-timestamp",
        "x-ca-signature": signature,
        "x-ca-timestamp": x_ca_timestamp,
        "x-ca-nonce": x_ca_nonce
    }
    data = []
    for person1 in existing_person:
        data.append({
        "personName": person1.personname,
        "gender": person1.gender,
        "orgIndexCode": person1.orgindexcode,
        "birthday": person1.birthday,
        "phoneNo": person1.phoneno,
        "email": person1.email,
        "certificateType": person1.certificatetype,
        "certificateNo": person1.certificateno,
        "jobNo": person1.jobno,
        "faces": [
            {
                "faceData": person1.faces
            }
        ]
    })
    return headers, data

@app.route(api_add_person_url, methods=['POST'])
def simulate_request_route():
    existingperson = person.query.all()
    headers, data = simulate_api_request()

    xcakey = headers.get('x-ca-key')
    xcasignatureheaders = headers.get('x-ca-signature-headers')
    xcasignature = headers.get('x-ca-signature')
    xcatimestamp = headers.get('x-ca-timestamp')
    xcanonce = headers.get('x-ca-nonce')

    sign_str = f"POST\n*/*\napplication/json\nx-ca-key:{xcakey}\nx-ca-nonce:{xcanonce}\nx-ca-timestamp:{xcatimestamp}\n{api_add_person_url}"

    if (
        xcakey != "22932116" or
        xcasignatureheaders != "x-ca-key,x-ca-nonce,x-ca-timestamp" or
        xcasignature != sign(appSecret, sign_str) or
        xcatimestamp != x_ca_timestamp or
        xcanonce != x_ca_nonce
    ):
        return jsonify({"error": f"请求失败，状态不正确"})

    # Handle data separately

    result = []
    for person2 in existingperson:
        result.append({
            "personId": person2.personid,
            "faceId": person2.facesid,
        })
    return {
    "code": "0",
    "msg": "success",
    "data": result
}
   
if __name__ == '__main__':
    app.run(debug=True)