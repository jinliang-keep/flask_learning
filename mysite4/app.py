# 2025-06-07
# 1.ORM模型与表的映射
# 2.ORM模型的CRUD操作

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# MySQL所在的主机名
# 如果MySQL服务器装在虚拟机里面，或是云服务器，在这里就要改成MySQL服务器的一个ip地址
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
PORT = 3306
# 连接MySQL的用户名
USERNAME = "root"
# 连接MySQL的密码
PASSWORD = "YOUR_PASSWORD"
# MySQL上创建的数据库名称
DATABASE = "database_learn"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

# 在app.config中设置好连接数据库的信息
# 然后使用SQLAlchemy(app)创建一个db对象
# SQLAlchemy会自动读取app.config中连接数据库的信息

# 创建一个叫做 db 的数据库工具对象
db = SQLAlchemy(app)

# 测试是否连接成功
# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute(text("select 1"))
#         print(rs.fetchone())  # (1,)

# 创建模型：表结构
class User(db.Model):
    #表名
    __tablename__ = "user"
    # 定义表中的字段/列
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # varchar
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    # 把所有表同步到数据库中
    db.create_all()

@app.route('/')
def home():
    return "Hello, 1222!"

# 增加数据
@app.route("/user/add")
def add_user():
    # 1.创建ORM对象
    # sql: insert user(username, password) values('张三', '333')
    user1 = User(username="张三", password="333")
    # 2.将ORM对象添加到db.session中
    db.session.add(user1)
    # 3.将db.session中的改变同步到数据库中
    db.session.commit()
    return "用户创建成功"

# 查询数据
@app.route("/user/query")
def query_user():
    # ①get查找：根据主键查找
    # user = db.session.get(User, 1)
    # user = User.query.get(1)
    # print(f"{user.id}:{user.username}-{user.password}")

    # ②filter_by查找
    # Query:类数组
    # WHERE username='张三'
    users = User.query.filter_by(username='张三')
    for user in users:
        print(user.username)
    return "数据查找成功!"

# 修改数据
@app.route("/user/update")
def update_user():
    user = User.query.filter_by(username='张三').first()
    user.password = '222'
    db.session.commit()
    return "数据修改成功！"

# 删除数据
@app.route('/user/delete')
def delete_user():
    user = User.query.get(1)
    db.session.delete(user)
    db.session.commit()
    return "数据删除成功！"

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = 8000)