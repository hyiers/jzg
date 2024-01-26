# coding=utf-8
from flask import Flask, request,jsonify
import json
from sqlalchemy import Column, String, create_engine, Integer, Text ,orm
from sqlalchemy.orm import sessionmaker,class_mapper
# from sqlalchemy.ext.declarative import declarative_base
import time
 
# 创建对象的基类:
Base = orm.declarative_base()

app = Flask(__name__)

def to_dict(obj):
    return dict((col.name, getattr(obj, col.name)) \
                for col in class_mapper(obj.__class__).mapped_table.c)

Base.to_dict=to_dict
# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'
 
    # 表的结构:
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    
    # sex = Column(String(4), nullable=False)
    # nation = Column(String(20), nullable=False)
    # birth = Column(String(8), nullable=False)
    # id_address = Column(Text, nullable=False)
    # id_number = Column(String(18), nullable=False)
    # creater = Column(String(32))
    # create_time = Column(String(20), nullable=False)
    # updater = Column(String(32))
    # update_time = Column(String(20), nullable=False, default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    #                      onupdate=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # comment = Column(String(200))
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'age': self.age}
    
# 初始化数据库连接:
engine = create_engine('postgresql://postgres:123456@localhost:5432/mydata')  # 用户名:密码@localhost:端口/数据库名
 
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
 
def createTable():
    # 创建表
    Base.metadata.create_all(engine)
 
 
def insertData():
    # 插入操作
    # 创建会话
    session = DBSession()
    # 创建新User对象:
    # local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    new_user = User(id=3,name='zs', age=25)
    # 添加到session:
    session.add(new_user)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()
 
@app.route('/insertLiData', methods=['GET'])   
def insertLiData():
    # 插入操作
    # 创建会话
    session = DBSession()
    # 创建新User对象:
    new_user = User(id=4, name='lisi', age=26)
    # 添加到session:
    session.add(new_user)
    # 提交即保存到数据库:
    session.commit()
    # 通过新的会话获取已插入的用户，避免DetachedInstanceError
    inserted_user = session.query(User).get(new_user.id)
    # 关闭session:
    session.close()
    
    return jsonify(inserted_user.to_dict())

@app.route('/selectData', methods=['GET']) 
def selectData():
    # 查询操作
    # 创建Session
    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    user = session.query(User).filter(User.id > '1' ).one()
    # print('name:', user.name)
    # print('id:', user.id)
    session.close()  # 关闭Session



    return jsonify(user.to_dict())
 
def updateData():
    # 更新操作
    session = DBSession()  # 创建会话
    users = session.query(User).filter_by(name="hsh4").first()  # 查询条件
    users.id_number = "abcd"  # 更新操作
    session.add(users)  # 添加到会话
    session.commit()  # 提交即保存到数据库
    session.close()  # 关闭会话
 
def deleteData():
    # 删除操作
    session = DBSession()  # 创建会话
    delete_users = session.query(User).filter(User.id == "1").first()
    if delete_users:
        session.delete(delete_users)
        session.commit()
    session.close()  # 关闭会话
 
def dropTable():
    # 删除表
    session = DBSession()  # 创建会话
    session.execute('drop table users')
    session.commit()
    session.close()
 
if __name__ == '__main__':   #表示py被直接执行，不是在其它模块中被导入执行的
    app.run(host='0.0.0.0', port=33027, debug=True)    
    # createTable()
    insertData()
    # updateData()
    # deleteData()
    # dropTable()
    print("hehe")
    selectData()