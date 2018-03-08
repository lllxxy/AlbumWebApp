from flask import Flask, url_for, render_template, redirect, session, request
import config
from exts import db
from models import *
from decoreators import login_required
from functions import *

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# 主页
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        # 用户信息
        user = User.query.filter(User.email == session.get('email')).first()
        # 获取相册
        albums = Album.query.filter(Album.user_id == user.id)
        return render_template('index.html',user=user, albums=albums)

    elif request.method == 'POST':
        user = User.query.filter(User.email == session.get('email')).first()
        AlbumName = request.form.get('AlbumName')
        Description = request.form.get('Description')
        # 检查相册名重复
        if Album.query.filter(Album.name == AlbumName, Album.user_id == user.id).first():
            return u'该相册名已存在'
        # 添加数据库表
        album = Album(
            name = AlbumName,
            description = Description,
            user_id = user.id
        )
        db.session.add(album)
        db.session.commit()
        album = Album.query.filter(Album.name == AlbumName, Album.user_id == user.id).first()
        return redirect(url_for('album',album_id = album.id))


# 登陆
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # 已经登陆时跳转回主页
    if session.get('email'):
        return redirect(url_for('index'))

    else:  # 未登陆时，进入登陆界面
        if request.method == 'GET':
            return render_template('login.html')
        else:
            input_email = request.form.get('email')
            input_password = request.form.get('password')
            user = User.query.filter(User.email == input_email, User.password == md5hex(input_password)).first()
            if user:
                session['email'] = user.email
                return redirect(url_for('index'))
            else:
                # 未注册或密码错误
                return render_template('login.html', Wrong='X')

# 注销
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))

# 注册
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
            # 成功后创建用户文件夹，位于css/images/<user_id>
            user_id = User.query.filter(User.email == email).first().id
            create_user_dir(user_id)
            return redirect(url_for('login'))

# 相册页面
@app.route('/album/<album_id>', methods=['GET','POST'])
def album(album_id):
    if request.method == 'POST':
        return u"Successful"
    else:
    #获取照片
        photos = Photo.query.filter_by(album_id=album_id)
        return render_template('album.html', photos=photos)