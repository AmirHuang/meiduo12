"""
.flask_script

- 解释: 属于flask扩展包
- 作用:
  - 1.通过命令方式启动程序,动态指定端口,ip,调试信息等
  - 2.配合flask_migrate做数据库的迁移(后天学习)

- 使用流程:
  - 1.安装扩展包
    - pip install flask_script
  - 2.导入Manager管理类
    - from flask_script import Manager
  - 3.创建manager对象,管理app
    - manager = Manager(app)
  - 4.启动程序
    - manager.run()

   5.通过命令脚本运行程序
    - python xxx.py runserver -h ip地址  -p 端口 -d调试模式


"""
from flask import Flask
from flask_script import Manager

app = Flask(__name__)

# app.config["DEBUG"] = True

class MyConfig(object):
    DEBUG = True
app.config.from_object(MyConfig)

#创建manager对象,管理app
manager = Manager(app)

@app.route('/')
def hello_world():

    return "helloworld"

if __name__ == '__main__':
    manager.run()