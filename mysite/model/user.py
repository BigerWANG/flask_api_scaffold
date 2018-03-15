#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : wang
# @File    : user.py
# @Software: PyCharm

from flask import g
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired,BadSignature
from mysite import config
from . import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False,index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    mobile = db.Column(db.String(11), nullable=True)
    cnname = db.Column(db.String(11), nullable=True)
    userdn = db.Column(db.String(200), nullable=True)

    @property
    def password(self):
        raise AttributeError("password write only")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_auth_token(self, expiration=config.PERMANENT_SESSION_LIFETIME):
        s = Serializer(config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id,"username":self.username})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        g.user = user
        return user

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username
