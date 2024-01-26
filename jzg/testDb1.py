from datetime import datetime

from flask import Flask
# 导入扩展包flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 配置数据库的连接信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/mydata'
# 关闭动态追踪修改的警告信息
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 展示sql语句
app.config['SQLALCHEMY_ECHO'] = True

# 实例化sqlalchemy对象，并且和程序实例关联
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    class GENDER:
        MALE = 0
        FEMALE = 1

    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
    mobile = db.Column(db.String, doc='手机号')
    password = db.Column(db.String, doc='密码')
    name = db.Column('user_name', db.String, doc='昵称')
    gender = db.Column(db.Integer, default=GENDER.FEMALE, doc='性别')
    birthday = db.Column(db.Date, doc='生日')
    is_delete = db.Column(db.Boolean, default=False, doc='是否删除')
    # 当模型类字段与表字段不一致，可在Column函数第一个参数指定
    time = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    update_time = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')

    # primaryjoin定义连接条件 : param1:另外一方类名 param2: 具体连接条件
    follows = db.relationship('Car', primaryjoin='User.id==foreign(Car.user_id)')


class Car(db.Model):
    __tablename__ = 'car'

    class TYPE:
        SUV = 0
        SEDAN = 1
        PICKUP = 2

    id = db.Column('car_id', db.Integer, primary_key=True, doc='主键ID')
    user_id = db.Column(db.Integer, doc='用户ID')
    type = db.Column(db.Integer, doc='类型')
    name = db.Column(db.String, doc='名称')
    price = db.Column(db.Numeric, default=0.00, doc='价格')


if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()