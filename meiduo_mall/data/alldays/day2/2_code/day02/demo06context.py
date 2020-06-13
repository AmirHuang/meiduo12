"""
flask中提供了两种类型上下文

- 请求上下文:
  - request: 和每次请求相关,封装的是这一次请求中所有相关的数据
  - session: 封装每个用户相关的信息,在服务器内部
- 应用上下文
  - current_app: 当前app对象,实际上就是app的代理对象,替代app处理相关的请求,获取相关的配置信息
    g: 一次完整请求中的一个容器, (在项目中,配合装饰器封装用户登陆数据)
"""
from flask import Flask,current_app,g

app = Flask(__name__)

@app.before_request
def before_request():
    g.name = "zhangsan"


@app.route('/')
def hello_world():

    print(app.config.get("DEBUG"))
    print(current_app.config.get("DEBUG"))

    print(g.name)

    return "helloworld"

if __name__ == '__main__':
    app.run(debug=True)
