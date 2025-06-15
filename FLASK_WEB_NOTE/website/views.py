# 设置网站的标准路由
# 非认证相关的页面
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
# 登录了才能访问主页
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) <= 1:
            flash('笔记太短！请输入1个字符以上的内容。', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('笔记已添加！', category='success')
    return render_template("home.html", user=current_user)

# 删除笔记路由
@views.route('/delete_note', methods=['POST'])
def delete_note():
    data = request.get_json()
    noteId = data.get('noteId')
    
    note = db.session.get(Note, noteId)

    if note and note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
