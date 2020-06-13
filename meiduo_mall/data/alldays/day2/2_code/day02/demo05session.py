"""
session

- 解释: 用来记录浏览器服务器交互数据,由服务器设置,存储在服务器,用来存储敏感数据,身份证,银行卡号,用户登陆状态等
- 设置:session[key] = value
- 获取:value = session.get(key)

注意点:

- 1.存储session数据的时候依赖于cookie,将sessionID存储到cookie中
- 2.sessionID是服务器内部session空间的一把钥匙
- 3.由于sessionID是存储在浏览器所以需要加密,需要用到秘钥(SECRET_KEY)

"""
from flask import Flask,session

app = Flask(__name__)
app.config["SECRET_KEY"] = "jfkdjfkdf"

#设置session
@app.route('/set_session/<name>')
def set_session(name):

    session["name"] = name

    return "设置session"

#获取session
@app.route('/get_session')
def get_session():

    name = session.get("name")

    return "设置session, name is %s"%name


if __name__ == '__main__':
    app.run(debug=True)