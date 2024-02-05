from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid
import time
import hmac
import hashlib
import base64
from sqlalchemy.orm import class_mapper

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/pt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class Org(db.Model):
    __tablename__ = 'org'
    orgindexcode = db.Column(db.String, primary_key=True)
    orgno = db.Column(db.String, nullable=True)
    orgname = db.Column(db.String, nullable=True)
    orgpath = db.Column(db.String, nullable=True)
    parentorgindexcode = db.Column(db.String, nullable=True)
    parentorgname = db.Column(db.String, nullable=True)
    updatetime = db.Column(db.String, nullable=True)

def org_to_dict(org):
    return {column.key: getattr(org, column.key) for column in class_mapper(org.__class__).mapped_table.c}

with app.app_context():
    db.create_all()

appSecret = "GSCOsNc7EMA61FfjE"
api_add_person_url = "/api/resource/v2/person/single/add"
api_origin_url = "/api/resource/v1/org/orgList"
x_ca_nonce = str(uuid.uuid4())
x_ca_timestamp = str(int(round(time.time()) * 1000))

def sign(key, value):
    temp = hmac.new(key.encode(), value.encode(), digestmod=hashlib.sha256)
    return base64.b64encode(temp.digest()).decode()

def get_root_org():
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
    headers = get_root_org()
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
        return jsonify({"error": f"0"})

    pageNo = 1
    pageSize = 10
    orgs = Org.query.all()
    start_index = (pageNo - 1) * pageSize
    end_index = start_index + pageSize
    paginated_orgs = [org_to_dict(org) for org in orgs[start_index:end_index]]

    result = {
        "code": "0",
        "msg": "ok",
        "data": {
            "total": len(orgs),
            "pageNo": pageNo,
            "pageSize": pageSize,
            "list": paginated_orgs
        }
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
