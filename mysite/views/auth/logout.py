#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/12/12 19:18
# @Author  : wangmengyu
# @File    : logout.py
# @Software: PyCharm

from .. import api
from flask import jsonify, session,g
from flask_restful import  Resource
from flask_babel import  gettext as _
from mysite.utils.public_utils import clear_user_cookie
from mysite.utils.logger import error_log as logerror

class User_logout(Resource):
    
    def post(self):
        try:
            g.user = None
            clear_user_cookie(session)
            return jsonify({"code": 20000, "msg": _("success")})
        except Exception, e:
            logmsg = "errormsg:%s"%e
            logerror.error(logmsg)
            return jsonify({"code": 50000, "msg": _("Internal Server Error")})
        
api.add_resource(User_logout, "/auth/logout")