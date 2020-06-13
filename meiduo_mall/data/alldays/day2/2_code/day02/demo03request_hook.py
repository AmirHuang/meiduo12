"""
请求钩子

- 解释: 在请求开始,或者结束的时候做一些准备或者收尾工作
- 常见的请求钩子有四种:
  - 1. before_first_request:在处理第一个请求前执行
  - 2. before_request:在每次请求前执行,在该装饰函数中,一旦return,视图函数不再执行
  - 3. after_request:如果没有抛出错误，在每次请求后执行
       接受一个参数：视图函数作出的响应
       在此函数中可以对响应值,在返回之前做最后一步处理,再返回
  - 4.teardown_request：在每次请求销毁后执行
    	接受一个参数:用来接收错误信息

"""
from flask import Flask, request

app = Flask(__name__)

#1.before_first_request:在处理第一个请求前执行
#特点: 在第一次访问的时候执行,适合做: 数据库的链接,文件的创建
@app.before_first_request
def before_first_request():
    print("before_first_request")

#2. before_request:在每次请求前执行,在该装饰函数中,一旦return,视图函数不再执行
#特点: 每次请求前都会执行, 适合统计视图函数的访问情况, 适合对请求的参数做校验
@app.before_request
def before_request():
    #取出浏览器请求参数
    token = request.args.get("token")

    #做校验
    if int(token) < 10:
        return "你是坏蛋"

    print("before_request")

#3. after_request:如果没有抛出错误，在每次请求后执行
#特点: 适合对数据的交互格式做统一处理
@app.after_request
def after_request(resp):
    print("after_request")
    resp.headers["Content-Type"] = "application/json"
    return resp

#4.teardown_request：在每次请求销毁后执行
#特点: 适合做服务器内部异常信息的统计
@app.teardown_request
def teardown_request(e):
    print(e)
    print("teardown_request")


@app.route('/')
def hello_world():

    return "helloworld"

if __name__ == '__main__':
    app.run(debug=True)