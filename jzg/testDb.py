# 使用flask_sqlalchemy进行数据库连接
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 配置数据库信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/mydata'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 生成数据库访问对象
db = SQLAlchemy(app)
db.init_app(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    name = db.Column(db.String(10))
    activate = db.Boolean(db.Boolean)
    heigh = db.Column(db.Float)

    def save(self):
        db.session.add(self)
        db.session.commit()
    def __str__(self):
        return self.name

class Phone(db.Model):
    __tablename__ = 'phone'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    content = db.Column(db.String(11))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))


    def save(self):
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return self.content


if __name__=="__main__":
    #  对表的操作 创建：# 删除：
    db.drop_all()
    db.create_all()
    user1 = User(name='小明',activate=True,heigh=1.5)
    user1.save()
    phone = Phone(content='12345678901',user_id=user1.id)
    phone.save()
    print(user1,phone)
