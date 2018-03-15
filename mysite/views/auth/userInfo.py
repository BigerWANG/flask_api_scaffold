#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/12/15 19:56
# @Author  : wangmengyu
# @File    : userInfo.py
# @Software: PyCharm

from .. import api
from flask import jsonify,g,session,current_app
from flask_restful import  Resource
from flask_babel import  gettext as _
from mysite.utils.logger import error_log as logerror
from mysite.utils.public_utils import clear_user_cookie

class User_userInfo(Resource):
    
    def get(self):
        try:
            if g.user:
                username = g.user.username
                if username in current_app.config.get("ADMINLIET", []):
                    admin = True
                else:
                    admin = False
                return jsonify({"code":20000,"msg":_("success"),"data":{"userName":username,"admin":admin}})
            else:
                logerror.error("session:%s;errmsg:g.user Not Found" % str(session))
                clear_user_cookie(session)
                return jsonify({"code": 40001, "msg": _("user not login")})
        except Exception,e:
            logerror.error("session:%s;errmsg:%s" % (str(session),e))
            clear_user_cookie(session)
            return jsonify({"code": 40001, "msg": _("user not login")})



api.add_resource(User_userInfo, "/auth/userInfo")