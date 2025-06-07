# 2025-06-05
# URL与视图的映射

from flask import Flask, request

app = Flask(__name__)

# url: http[80端口]/https[443端口]://www.baidu.com:443（端口号可加可不加）/path(路径)
# （①协议：http/https）
# （②域名：www.baidu.com）
# 因为别的部分都不需要我们去修改，所以url与试图也可以叫做path与视图

# 把路由跟视图函数进行映射
# 装饰器
@app.route('/')
def home():
    return "Hello, 1222!"

@app.route("/profile")
def profile():
    return "我是个人中心！"

@app.route("/blog/list")
def blog_list():
    return "我是博客列表！"

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


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = 8000)