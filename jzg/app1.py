from flask import Flask
"""
flask路由
"""

app = Flask(__name__)

@app.route('/')
def index():
    return "Helo World!"

@app.route('/hello/<name>')
def helo_name(name):
    return 'Helo %s!' % name

if __name__ == '__main__':   #表示py被直接执行，不是在其它模块中被导入执行的
    app.run(debug=True)                