from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/jzg"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    gh = db.Column(db.String(20), nullable=True)
    xm = db.Column(db.String(10), nullable=True)
    bmdm = db.Column(db.String(20), nullable=True)
    bmcc = db.Column(db.String(20), nullable=True)
    dwh = db.Column(db.String(20), nullable=True)
    dwmc = db.Column(db.String(20), nullable=True)
    ryztm = db.Column(db.String(20), nullable=True)
    ryztm_mc = db.Column(db.String(20), nullable=True)
    lxdh = db.Column(db.String(20), nullable=True)

with app.app_context():
    db.create_all()

@app.route('/9044143925417/data_center/dwd/gxjg/jzgjcsj', methods=['GET'])
def get_employee_data():
    auth_id = request.headers.get('X-H3C-ID')
    auth_key = request.headers.get('X-H3C-APPKEY')

    if auth_id != "9044143925417" or auth_key != "sakvxb36":
        print("Authentication failed")
        return jsonify({"error": "Authentication failed"}), 401
    

    employees = Employee.query.all()
    result = []
    for employee in employees:
        result.append({
            "gh": employee.gh,
            "xm": employee.xm,
            "bmdm": employee.bmdm,
            "bmcc": employee.bmcc,
            "dwh": employee.dwh,
            "dwmc": employee.dwmc,
            "ryztm": employee.ryztm,
            "ryztm_mc": employee.ryztm_mc,
            "lxdh": employee.lxdh
        })

    print("Authentication successful")
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, sort_keys=False),
        status=200,
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=33027, debug=True)
