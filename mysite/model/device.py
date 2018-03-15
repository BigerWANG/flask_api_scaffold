#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : wang
# @File    : device.py
# @Software: PyCharm

from . import db
import datetime


class AgentDevice(db.Model):
    __tablename__ = 'device'
    
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(100), index=True)
    ip = db.Column(db.String(20), index=True, unique=True)
    version = db.Column(db.String(50), default="v2.0.10")
    status = db.Column(db.String(20), default="up")
    msg = db.Column(db.String(500), default="")
    updateTime = db.Column(db.DateTime(), default=datetime.datetime.now)
    uploadTime = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    def __repr__(self):
        return '<AgentDevice %r>' % self.ip
