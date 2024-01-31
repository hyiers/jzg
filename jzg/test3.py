from flask import Flask, request
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

def sign(key, value):
    temp = hmac.new(key.encode(), value.encode(), digestmod=hashlib.sha256)
    return base64.b64encode(temp.digest()).decode()

def validate_request_headers(headers, method, url):
    # Reconstruct the signature string
    sign_str = f"{method}\n*/*\napplication/json\n"
    for header_key, header_value in headers.items():
        if header_key.startswith("x-ca-"):
            sign_str += f"{header_key.lower()}:{header_value}\n"
    sign_str += f"{url}"

    # Generate the signature
    signature = sign(appSecret, sign_str)

    # Validate the generated signature against the received signature
    if headers.get("x-ca-signature") == signature:
        return True
    else:
        return False

def simulate_api_request(headers):
    print("simulate_api_request function called") 
    appKey = "22932116"
    api_add_person_url = "/api/resource/v2/person/single/add"
    x_ca_nonce = str(uuid.uuid4())
    x_ca_timestamp = str(int(round(time.time()) * 1000))

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
    response = requests.post(base_url + api_add_person_url, json=request_data, headers=headers)
    return response

@app.route('/api/resource/v2/person/single/add', methods=['POST'])
def simulate_request_route():
    # Validate the headers
    if validate_request_headers(request.headers, request.method, request.url):
        print("Headers are valid. Authentication successful.")
        
        # Call simulate_api_request with the validated headers
        response1 = simulate_api_request(request.headers)
        print(response1)

        return "Authentication successful."
    else:
        return "Headers are not valid. Authentication failed."

if __name__ == '__main__':
    app.run(debug=True)
