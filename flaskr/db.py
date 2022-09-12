from email.mime import application
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

db = SQLAlchemy()
class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    posts = db.relationship('posts', backref='author_id', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.id}, Username {self.username}>"

class PostModel(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime(timezone=False), nullable=False, default=func.now())
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    readtime = db.Column(db.DateTime(timezone=False), nullable=True, default=None)
    otp = db.Column(db.String(8), nullable=True, default=None)

    def __init__(self, author_id, title, body, otp):
        self.author_id = author_id
        self.title = title
        self.body = body
        self.otp = otp

    def __repr__(self):
        return f"<Post: {self.id}, Author: {self.author_id}, Created: {self.created}, Title: {self.title}, body: {self.body}, readtime: {self.readtime}, otp: {self.otp}>"