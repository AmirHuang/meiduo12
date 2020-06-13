"""
状态保持

- 解释: 浏览器的http协议,默认是无状态的,不知道曾经访问过什么
- 实现有状态的两种方式:
  - cookie
    - 解释: 用来记录浏览器和服务器之间的交互数据,由服务器进行设置,存储在浏览器的
    - 设置:response.set_cookie(key,value,max_age)
      - max_age: 有效期,单位是秒,如果不指定默认就是一次浏览器会话结束
    - 获取:request.cookies.get(key)
  -

"""
from flask import Flask, make_response, request

app = Flask(__name__)

#设置cookie
@app.route('/set_cookie')
def set_cookie():

    #获取响应体的对象
    response = make_response("set_cookie")

    #设置cookie
    response.set_cookie("computer","lenovo")
    response.set_cookie("wawa","baby",10)

    return response

#获取cookie
@app.route('/get_cookie')
def get_cookie():

    #获取cookie
    computer = request.cookies.get("computer")
    wawa = request.cookies.get("wawa")

    return "computer is %s, wawa is %s"%(computer,wawa)



if __name__ == '__main__':
    app.run(debug=True)