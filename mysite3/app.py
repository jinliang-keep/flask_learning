# 2025-06-05 - 2025-06-07
# 【jinja2】
# 1.模板渲染
# 2.模板访问对象属性
# 3.过滤器的使用
# 4.控制语句
# 5.模板继承
# 6.加载静态文件

from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# 自定义一个过滤器，转换时间格式
def datetime_format(value, format="%Y年%m月%d日 %H:%M"):
    return value.strftime(format)

app.add_template_filter(datetime_format,"dformat")

# 创建一个类
class User:
    def __init__(self,username,email):
        self.username = username
        self.email = email

@app.route('/')
def hello_world():
    user = User(username="金金", email="jinliang@qq.com")
    person = {
        "username": "张三",
        "email": "zhangsan@qq.com"
    }
    return render_template("index.html", user=user, person=person)

# 带参数的URL：将参数固定到了path中
@app.route("/blog/<int:blog_id>")
def blog_detail(blog_id):
    return "您访问的博客是： %s" % blog_id

# 查询字符串的方式传参：这种传参的方式更加灵活，在定义url的时候不用定义这个参数，再通过视图函数request.args就可以获取到这个参数
# 还可以定义传参的方式，get请求、post请求
# 有时候参数可传可不传
# 未带参数：/book/list: （我没有带任何的参数，但）会给我返回第1页的数据
# 带了参数：/book/list?page=2: 获取第2页的数据（这里通过“?”传参）
@app.route('/book/list')
def book_list():
    # arguments：参数
    # request.arg：类字典类型
    page = request.args.get("page", default=1, type=int)
    return f"您获取的是第{page}的图书列表！"

# 过滤器
@app.route("/filter")
def filter_demo():
    user = User(username="金金", email="jinliangx@qq.com")
    mytime = datetime.now()
    return render_template("filter.html", user=user, mytime=mytime)

# 控制语句
@app.route("/control")
def control_statement():
    age = 23
    books = [{
        "name": "语文书",
        "author": "人民教育出版社"
    },{
        "name": "雅思王听力",
        "author": "王陆"
    },]
    return render_template("control.html", age=age, books=books)

# 模板继承
@app.route("/child1")
def child1():
    return render_template("child1.html")

# 模板继承
@app.route("/child2")
def child2():
    return render_template("child2.html")

# 加载静态文件
@app.route('/static')
def static_demo():
    return render_template("static.html")

if __name__ == '__main__':
    app.run(debug=True)