"""
SQLAlchemy models
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('message_id', db.Integer, db.ForeignKey('message.id'), primary_key=True)
                )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(120), unique=True, nullable=False)
    messages = db.relationship('Message', backref='user', lazy=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False)
    messages = db.relationship('Message', backref='post')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(10000000), nullable=False)
    sent = db.Column(db.DateTime, nullable=False)
    received = db.Column(db.DateTime, nullable=False)

    user_number = db.Column(db.String, db.ForeignKey('user.number'))

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    tags = db.relationship('Tag', secondary=tags, backref=db.backref('messages'))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(1000), nullable=False)





