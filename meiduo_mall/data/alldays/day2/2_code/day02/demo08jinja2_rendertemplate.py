"""
jinja2模板

- 用来提供页面的展示
- 好处:
  - 1.视图函数负责数据,业务处理
  - 2.模板负责数据的展示
- 使用:
  - 通过render_template()函数渲染页面
  - 格式: render_template('模板文件名',key=value)

"""
from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def hello_world():

    return render_template("file01hello.html")

if __name__ == '__main__':
    app.run(debug=True)