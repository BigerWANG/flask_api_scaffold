#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/12/8 15:52
# @Author  : wangmengyu
# @File    : __init__.py.py
# @Software: PyCharm


from flask import Blueprint
from flask_restful import Api
from mysite import config

Api_Blueprint = Blueprint('api', __name__, url_prefix='/api/%s'%config.RESTFUL_API_VERSION)
api = Api()
api.init_app(Api_Blueprint)


import auth.login
import auth.logout
import auth.copInfo
import auth.userInfo

import agent.agentList