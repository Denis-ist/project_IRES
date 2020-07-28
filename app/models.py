# -*- coding: utf-8 -*-
from app import db
# from werkzeug import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    name = db.Column(db.String)
    password_hash = db.Column(db.String())
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    about_me = db.Column(db.String)
    posts = db.relationship('Post', backref='author', lazy="dynamic")  # Post.author
    address = db.relationship('Address', uselist=False, backref='user')  # Address.user

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String())
    city = db.Column(db.String())
    street = db.Column(db.String())
    house_number = db.Column(db.Integer())
    address_index = db.Column(db.Integer())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    post = db.relationship('Post', lazy='dynamic')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(120))
    intro_text = db.Column(db.String)
    text = db.Column(db.String)
    date_created = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category')

    def to_dict(self):
        return {
            'userId': self.author_id,
            'id': self.id,
            'title': self.heading,
            'body': self.intro_text
        }

    def __repr__(self):
        return f'<Post "{self.heading}">'


