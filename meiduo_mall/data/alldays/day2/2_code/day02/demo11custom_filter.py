"""
自定义过滤器

- 解释: 当系统提供的过滤器满足不了需求,就自定义
- 自定义过滤器有两种方式
  - 1.先定义函数,再将函数添加到过滤器列表中
  - def func():pass
  - app.add_template_filter(函数名,过滤器名字)

  - 2.定义函数的时候,就使用过滤器装饰
  - @app.template_filter(过滤器名字) def func():pass

需求:
1.求列表中所有偶数和
2.实现列表反转

"""
from flask import Flask,render_template

app = Flask(__name__)

#1.先定义函数,再将函数添加到过滤器列表中
def oushu_sum(list):

    sum = 0
    for item in list:
        if item %2 == 0:
            sum += item
    return sum

app.add_template_filter(oushu_sum,"OUSHU_SUM")

# 2.定义函数的时候, 就使用过滤器装饰
@app.template_filter("my_reverse")
def reverse_function(list):
    list.reverse()
    return list

@app.route('/')
def hello_world():

    return render_template("file04custom_filter.html")

if __name__ == '__main__':
    app.run(debug=True)