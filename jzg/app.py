from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#mysql配置 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True       #避免警告

db = SQLAlchemy(app)

from app import db

class User(db.Modle):
    gh = db.Column(db.String(20),primary_key = True)
    xm = db.Column(db.String(),nullable = True)
    bmdm = db.Column(db.String,nullable = True)
    bmcc = db.Column(db.String,nullable = True)
    dwh = db.Column(db.String,nullable = True)
    dwmc = db.Column(db.String,nullable = True)
    ryztm = db.Column(db.String,nullable = True)
    ryztm_mc = db.Column(db.String,nullable = True)
    lxdh = db.Column(db.String,nullable = True)


db.create_all()

@app.route('/9044143925417/data_center/dwd/gxjg/jzgjcsj', methods=['GET'])              #使用装饰器url配置    访问：   IP：port/
def get_employee_data():           
    # 静态Token验证
    x_h3c_id = request.headers.get('X-H3C-ID')    
    x_h3c_appkey = request.headers.get('X-H3C-APPKEY')
    if x_h3c_id != "9044143925417" or x_h3c_appkey != "sakvxb36":
        return jsonify({"error": "Authentication failed"}), 401
    
    # 查询数据库并构造响应
    
    
    return jsonify(result)

if __name__ == '__main__':   #表示py被直接执行，不是在其它模块中被导入执行的
    app.run(host='0.0.0.0', port=33027, debug=True)               
