# 认证相关的页面
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

# 登录
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # 数据库中寻找用户
        user = User.query.filter_by(email=email).first()
        if user:
            # 判断密码是否正确
            if check_password_hash(user.password, password):
                flash(f'您好，{user.first_name}！您已成功登录！',category='success')
                # 记住用户的登录状态
                remember = True if request.form.get('remember') else False
                login_user(user, remember=remember)
                return redirect(url_for('views.home'))
            else:
                flash('密码不正确，请尝试重新输入！', category='error')
        else:
            flash('邮箱不存在！', category='error')

    return render_template("login.html", user=current_user)

# 登出
@auth.route('/logout')
# 确保只有已登陆的用户才能访问此页面/路由
@login_required
def logout():
    logout_user()
    flash(f'您已退出登录！',category='success')
    return redirect(url_for('auth.login'))

# 注册
@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        # 查询注册邮箱是否存在于数据库中
        if user:
            flash('此邮箱已被注册！', category='error')
        elif len(email) < 4:
            flash('邮箱必须大于3个字符', category='error')
        elif len(firstName) <2:
            flash('用户名必须大于1个字符', category='error')
        elif len(password1) < 7:
            flash('密码必须大于6个字符', category='error')
        elif password1 != password2:
            flash('与首次输入的密码不一致', category='error')
        # 创建新用户
        else:
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            # 用户注册成功后，自动登录
            # # 记住用户的登录状态
            remember = True if request.form.get('remember') else False
            login_user(user, remember=remember)
            flash('账号创建成功！', category='success')

            return redirect(url_for('views.home'))
            
    return render_template("sign_up.html", user=current_user) 