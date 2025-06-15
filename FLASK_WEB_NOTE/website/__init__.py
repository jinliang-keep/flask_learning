from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from dotenv import load_dotenv
from flask_login import LoginManager

db =SQLAlchemy()
# DB_NAME = "database.db"

load_dotenv()

def create_app():
    app = Flask(__name__)

    # 数据库配置
    secret_key = os.getenv("SECRET_KEY")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = int(os.getenv("DB_PORT", 3306))
    db_name = os.getenv("DB_NAME")
    
    app.config['SECRET_KEY'] = secret_key

    DATABASEURI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASEURI
    db.init_app(app)

    # 注册蓝图
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # 创建数据库
    from .models import User, Note

    create_database(app)

    # 登录状态的自动记忆与验证
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = u"请先登录后再访问此页面！" # 自定义中文提示
    login_manager.init_app(app)
        
    @login_manager.user_loader # 从数据库中寻找用户
    def load_user(id):
        return User.query.get(int(id))

    return app

# 创建数据库
def create_database(app):
    with app.app_context():
        db.create_all()
    print('数据库已创建！')