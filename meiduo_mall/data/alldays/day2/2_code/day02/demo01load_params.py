"""
加载应用程序app的参数

- 共有三种方式:
  - app.config: 使用应用程序中,所有的配置参数
  - 1.从配置类中加载参数信息
    - app.config.from_object(配置类)
  - 2.从配置文件中加载参数信息
    - app.config.from_pyfile(配置文件)
  - 3.从环境变量中加载配置信息(了解)
    - app.config.from_envvar("环境变量key")

"""
from flask import Flask

app = Flask(__name__)

#定义配置类
class MyConfig(object):
    DEBUG = True

#1.从配置类中加载参数信息
# app.config.from_object(MyConfig)

#2.从配置文件中加载参数信息
# app.config.from_pyfile("config.ini")

#3.从环境变量中加载配置信息
app.config.from_envvar("FLASKING")

@app.route('/')
def hello_world():
    print(app.config.get("DEBUG"))
    return "helloworld"

if __name__ == '__main__':
    app.run()