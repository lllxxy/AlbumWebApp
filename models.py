from exts import db
from datetime import datetime


class User(db.Model):

    __tablename__ = 'user'
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email         = db.Column(db.String(30), nullable=False)
    username      = db.Column(db.String(30), nullable=False)
    password      = db.Column(db.String(100), nullable=False)
    regdate       = db.Column(db.DateTime, default=datetime.now)


class Album(db.Model):

    __tablename__ = 'album'
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name          = db.Column(db.String(100), nullable = False)
    description   = db.Column(db.Text)
    credate       = db.Column(db.DateTime, default=datetime.now)
    del_sign      = db.Column(db.String(1))


    user_id       = db.Column(db.Integer, db.ForeignKey('user.id'))
    author        = db.relationship('User', backref = db.backref('albums'))


class Photo(db.Model):

    __tablename__ = 'photo'
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path          = db.Column(db.String(200), nullable = False)
    description   = db.Column(db.Text)
    credate       = db.Column(db.DateTime, default=datetime.now)
    del_sign      = db.Column(db.String(1))

    album_id      = db.Column(db.Integer, db.ForeignKey('album.id'))
    album         = db.relationship('Album', backref = db.backref('photos'))


class Comment(db.Model):

    __tablename__ = 'comment'
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id       = db.Column(db.Integer, db.ForeignKey('user.id'))
    author        = db.relationship('User', backref=db.backref('comments'))

    photo_id      = db.Column(db.Integer, db.ForeignKey('photo.id'))
    photo         = db.relationship('Photo', backref=db.backref('comments'))

    del_sign = db.Column(db.String(1))
