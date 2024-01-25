from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#mysql配置 


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "MYSQL://"

db = SQLAlchemy(app)

@app.route('/')              #使用装饰器url配置    访问：   IP：port/
def hello_world():           #视图函数
   
    return 'Hello World'     #响应给浏览器的内容

if __name__ == '__main__':   #表示py被直接执行，不是在其它模块中被导入执行的
    app.run(debug=True)                
