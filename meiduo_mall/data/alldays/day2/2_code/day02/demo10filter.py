"""
- .jinja2中过滤器
  - 过滤器: 相当于python中的函数一样
  - 自带过滤器有两种:
    - 字符串过滤器
      - 使用格式: {{字符串 | 过滤器}}
      - 字符串过滤器:
        - title: 每个单词的首字母大写
        - lower: 单词字母转小写
        - reverse:反转
        - ...
    - 列表过滤器
      - 使用格式: {{列表 | 过滤器}}
      - 列表过滤器
        - length: 求列表长度
        - sum: 请求列表和
        - first: 列表第一个元素
        - ....

"""
from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def hello_world():

    return render_template("file03filter.html")

if __name__ == '__main__':
    app.run(debug=True)