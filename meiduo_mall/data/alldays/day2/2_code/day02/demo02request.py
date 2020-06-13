"""
- request.data: 获取的是以post提交的,非表单数据
- request.form: 获取的是以post提交的,表单数据
- request.args: 获取的是查询参数,一般是GET请求,获取的是问号后面拼接的参数
  - www.baidu.com?name=laowang&age=13

- request.method: 获取的是请求方式
- request.url: 获取的是浏览器的请求地址
- request.files: 获取的是form表单中input标签,type类型为file的值
- reuqest.cookies: 浏览器中的所有cookie信息

"""
from flask import Flask, request

app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def hello_world():

    # - 1. request.data: 获取的是以post提交的, 非表单数据
    print(request.data)

    # - 2. request.form: 获取的是以post提交的, 表单数据
    print(request.form)

    # - 3. request.args: 获取的是查询参数, 一般是GET请求, 获取的是问号后面拼接的参数
    print(request.args)
    # print(request.args["name"]) #不建议这中方式
    # print(request.args.get("name","banzhang"))# 建议使用该方式,取不到不会报错,返回None,加上后面参数,如果取不到使用默认值

    # - 4. request.method: 获取的是请求方式
    print(request.method)

    # - 5. request.url: 获取的是浏览器的请求地址
    print(request.url)

    return "helloworld"

if __name__ == '__main__':
    app.run(debug=True)