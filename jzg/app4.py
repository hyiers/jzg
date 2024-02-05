from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
import time
import hmac
import hashlib
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/pt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

x_ca_nonce = str(uuid.uuid4())
x_ca_timestamp = str(int(round(time.time()) * 1000))

class Person(db.Model):
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

class Org(db.Model):
    __tablename__ = 'org'
    orgindexcode = db.Column(db.String, primary_key=True)
    orgno = db.Column(db.String, nullable=True)
    orgname = db.Column(db.String, nullable=True)
    orgpath = db.Column(db.String, nullable=True)
    parentorgindexcode = db.Column(db.String, nullable=True)
    parentorgname = db.Column(db.String, nullable=True)
    updatetime = db.Column(db.String, nullable=True)

with app.app_context():
    db.create_all()

appSecret = "GSCOsNc7EMA61FfjE"
api_add_person_url = "/api/resource/v2/person/single/add"
api_origin_url = "/api/resource/v1/org/rootOrg"

def sign(key, value):
    temp = hmac.new(key.encode(), value.encode(), digestmod=hashlib.sha256)
    return base64.b64encode(temp.digest()).decode()

def get_root_org_headers():
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
    
    return headers
@app.route(api_origin_url, methods=['POST'])
def orign_request_route():
    headers = get_root_org_headers()
    sign_str = f"POST\n*/*\napplication/json\nx-ca-key:{headers['x-ca-key']}\nx-ca-nonce:{headers['x-ca-nonce']}\nx-ca-timestamp:{headers['x-ca-timestamp']}\n{api_add_person_url}"

    if any(
        headers[key] != value
        for key, value in {
            'x-ca-key': '22932116',
            'x-ca-signature-headers': 'x-ca-key,x-ca-nonce,x-ca-timestamp',
            'x-ca-signature': sign(appSecret, sign_str),
            'x-ca-timestamp': headers['x-ca-timestamp'],
            'x-ca-nonce': headers['x-ca-nonce']
        }.items()
    ):
        return jsonify({"error": "0"})

    add_data_to_org()

    org_data = Org.query.all()
    body = [{
        "orgIndexCode": org.orgindexcode,
        "orgNo": org.orgno,
        "orgName": org.orgname,
        "orgPath": org.orgpath,
        "parentOrgIndexCode": org.parentorgindexcode,
        "parentOrgName": org.parentorgname,
        "updateTime": org.updatetime
    } for org in org_data]

    return {"code": "0", "msg": "success", "data": body}

def get_org_index_code():
    response = app.test_client().post(api_origin_url, headers=get_root_org_headers())
    org_data = response.get_json()
    return [org["orgIndexCode"] for org in org_data.get("data", [])] if "data" in org_data else None

def add_data_to_org():
    if not Org.query.first():
        new_org = Org(
            orgindexcode="1234567890",
            orgno=" ",
            orgname=" ",
            orgpath=" ",
            parentorgindexcode=" ",
            parentorgname=" ",
            updatetime="2024-02-04"
        )
        db.session.add(new_org)
        db.session.commit()

def simulate_api_request():
    existing_person = Person.query.all()
    appKey = "22932116"
    org_index_code = get_org_index_code()

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
    
    data = [{
        "personName": person.personname,
        "gender": person.gender,
        "orgIndexCode": person.orgindexcode,
        "birthday": person.birthday,
        "phoneNo": person.phoneno,
        "email": person.email,
        "certificateType": person.certificatetype,
        "certificateNo": person.certificateno,
        "jobNo": person.jobno,
        "faces": [{"faceData": person.faces}]
    } for person in existing_person if person.orgindexcode not in org_index_code]

    return headers, data

@app.route(api_add_person_url, methods=['POST'])
def simulate_request_route():
    existing_person = Person.query.all()
    headers, data = simulate_api_request()

    if headers is None:
        return data  # Return the error response

    sign_str = f"POST\n*/*\napplication/json\nx-ca-key:{headers['x-ca-key']}\nx-ca-nonce:{headers['x-ca-nonce']}\nx-ca-timestamp:{headers['x-ca-timestamp']}\n{api_add_person_url}"

    if any(
        headers[key] != value
        for key, value in {
            'x-ca-key': '22932116',
            'x-ca-signature-headers': 'x-ca-key,x-ca-nonce,x-ca-timestamp',
            'x-ca-signature': sign(appSecret, sign_str),
            'x-ca-timestamp': headers['x-ca-timestamp'],
            'x-ca-nonce': headers['x-ca-nonce']
        }.items()
    ):
        return jsonify({"error": "0"})

    result = [{
        "personId": person.personid,
        "faceId": person.facesid,
    } for person in existing_person]

    return {"code": "0", "msg": "success", "data": result}

if __name__ == '__main__':
    app.run(debug=True)

