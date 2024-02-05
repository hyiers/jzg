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
#创建，链接连个数据库
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

#使用的AS，URL
appSecret = "GSCOsNc7EMA61FfjE"
api_add_person_url = "/api/resource/v2/person/single/add"
api_origin_url = "/api/resource/v1/org/rootOrg"
#时间戳等信息
x_ca_nonce = str(uuid.uuid4())
x_ca_timestamp = str(int(round(time.time()) * 1000))
#定义签名生成方式
def sign(key, value):
    temp = hmac.new(key.encode(), value.encode(), digestmod=hashlib.sha256)
    return base64.b64encode(temp.digest()).decode()


 #发送组织请求头
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

#接受获取组织列表请求    
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
    print(paginated_orgs)
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

#返回组织列表函数
def get_org_index_code():
    response = app.test_client().post(api_origin_url, headers=get_root_org())
    org_data = response.get_json()

    if "data" in org_data:
        return [org["orgindexcode"] for org in org_data["data"]["list"]]
    else:
        return None


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

#请求头生成函数
def simulate_api_request():
    existing_person = person.query.all()
    appKey = "22932116"
    # 得到组织列表
    org_index_code = get_org_index_code()

    sign_str = f"POST\n*/*\napplication/json\nx-ca-key:{appKey}\nx-ca-nonce:{x_ca_nonce}\nx-ca-timestamp:{x_ca_timestamp}\n{api_add_person_url}"
    signature = sign(appSecret, sign_str)

    # 请求头信息
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
        if person1.orgindexcode not in org_index_code:
            
            new_org = Org(
                orgindexcode=person1.orgindexcode,
                orgno=" ",
                orgname=" ",
                orgpath=" ",
                parentorgindexcode=" ",
                parentorgname=" ",
                updatetime=" "
            )
            db.session.add(new_org)
            db.session.commit()

            org_index_code.append(person1.orgindexcode)
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
            "faces": [{"faceData": person1.faces}]
        })

    return headers, data
 

#接受获取人员列表请求    
@app.route(api_add_person_url, methods=['POST'])
def simulate_request_route():
    existingperson = person.query.all()
    headers, data = simulate_api_request()

    if headers is None:
        return data  # Return the error response

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