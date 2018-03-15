#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/12/20 16:29
# @Author  : wangmengyu
# @File    : db_init.py
# @Software: PyCharm

import os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from mysite.model import db
from mysite.model.user import User
from mysite.model.device import AgentDevice
from mysite import app

try:
    db.create_all(app=app)
    print "Create Tables OK"
except Exception,e:
    print "Create Tables Failed\n%s"%e