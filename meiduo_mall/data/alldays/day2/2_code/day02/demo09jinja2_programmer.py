"""
- 模板语法
  - 1.获取变量的值
    - {{变量名}}
    - 和vue里面的'小胡子'语法类似
  - 2.分支语句if
    - {%if 条件%} 内容 {%endif%}
    - {%if 条件%} 内容  {%elif 条件%} 内容 {%else%} 内容  {%endif%}
  - 3.循环语句for
    - {%for 变量 in 容器%} 内容 {%endfor%}
  - 4.注释
    - {# 注释内容 #}

"""
from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def hello_world():

    #定义数据
    num = 10
    str = "隔壁老王在练腰"
    tuple = (1,2,3,4)
    list = [5,6,7,8,9]
    dict = {
        "name":"班长",
        "age":29
    }

    #携带数据渲染页面
    return render_template("file02program.html",num=num,str=str,tuple=tuple,list=list,dict=dict)

if __name__ == '__main__':
    app.run(debug=True)