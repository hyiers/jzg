from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 数据库配置
HOSTNAME = '127.0.0.1'
PORT = '5432'
DATABASE = 'mydata'
USERNAME = 'postgresql'
PASSWORD = '123456'

DB_URI = 'postgresql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# 定义数据表类
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
#根据id查询
user=User.query.get(1)#查询id为1的用户
    
# 查询所有用户
all_users = User.query.all()
#遍历
for user in all_users:
	print(f'{user.id}:{user.name}:{user.age}')
    
# 查询指定用户
user = User.query.filter_by(name='John').first()

# 查询年龄在20到30之间的用户
users = User.query.filter(User.age >= 20, User.age <= 30).all()