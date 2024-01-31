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
appSecret = "GSCOsNc7EMA61FfjE"
api_add_person_url = "/api/resource/v2/person/single/add"
x_ca_nonce = str(uuid.uuid4())
x_ca_timestamp = str(int(round(time.time()) * 1000))

def sign(key, value):
    temp = hmac.new(key.encode(), value.encode(), digestmod=hashlib.sha256)
    return base64.b64encode(temp.digest()).decode()

def simulate_api_request():
    print("simulate_api_request function called") 
    appKey = "22932116"
    #print(auth_id)

    # Example request data
    request_data = {"name": "John Doe", "age": 30}
    print("Authentication successful")

    # Construct the signature string
    sign_str = f"POST\n*/*\napplication/json\nx-ca-key:{appKey}\nx-ca-nonce:{x_ca_nonce}\nx-ca-timestamp:{x_ca_timestamp}\n{api_add_person_url}"

    # Generate the signature
    signature = sign(appSecret, sign_str)

    # Construct request headers
    headers = {
        "Accept": "*/*",
        'Content-Type': 'application/json',
        "x-ca-key": appKey,
        "x-ca-signature-headers": "x-ca-key,x-ca-nonce,x-ca-timestamp",
        "x-ca-signature": signature,
        "x-ca-timestamp": x_ca_timestamp,
        "x-ca-nonce": x_ca_nonce
    }

    # Send the request
    return headers

    

@app.route(api_add_person_url, methods=['POST'])
def simulate_request_route():
    rheaders = simulate_api_request()
    
    xcakey = rheaders.get('x-ca-key')
    xcasignatureheaders = request.headers.get('x-ca-signature-headers')
    xcasignature = request.headers.get('x-ca-signature')
    xcatimestamp = request.headers.get('x-ca-timestamp')
    xcanonce = request.headers.get('x-ca-nonce')

    sign_str = f"POST\n*/*\napplication/json\nx-ca-key:{xcakey}\nx-ca-nonce:{xcanonce}\nx-ca-timestamp:{xcatimestamp}\n{api_add_person_url}"

    print (xcakey)
    if xcakey != "22932116":
        return {"error": f"Request failed with status"}
    return 1

    # Check the status code
    #if response1.status_code == 200:
        # Parse the response and return the data
    #    return response1.json()
    #else:
        # Handle the error status code
    #    return {"error": f"Request failed with status code {response.status_code}"}


    return jsonify(1)

if __name__ == '__main__':
    app.run(debug=True)
