from flask import Flask, url_for, render_template, redirect, session, request
import config
from exts import db
from models import *
import hashlib
from decoreators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# 加密密码
def md5hex(password):
    if not isinstance(password, str):
        password = str(password)
    password = 'ThisIsPassWord' + password
    password = password.encode('utf-8')
    m = hashlib.md5()
    m.update(password)
    return m.hexdigest()

@app.route('/')
@login_required
def index():
    user = User.query.filter(User.email == session.get('email')).first()
    return render_template('index.html',user=user)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    # 已经登陆时跳转回主页
    if session.get('email'):
        return redirect(url_for('index'))

    else:  # 未登陆时，进入登陆界面
        if request.method == 'GET':
            return render_template('login.html',user=None)
        else:
            input_email = request.form.get('email')
            input_password = request.form.get('password')
            user = User.query.filter(User.email == input_email, User.password == md5hex(input_password)).first()
            if user:
                session['email'] = user.email
                return redirect(url_for('index'))
            else:
                # 未注册或密码错误
                return u'Wrong Password or user'

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        email = request.form.get('email')
        nickname = request.form.get('nickname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        assert email
        assert nickname
        assert password1
        assert password2

        if password1 != password2:
            return u'Password1 unequal with Password2'

        user = User.query.filter(User.email == email).first()
        if user:
            return u'This Email was registed'
        else:
            user = User(
                email = email,
                username = nickname,
                password = md5hex(password1)
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
