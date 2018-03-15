#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/12/15 19:55
# @Author  : wangmengyu
# @File    : copInfo.py
# @Software: PyCharm

from .. import api
from flask import jsonify, g,current_app,session
from flask_restful import  Resource
from mysite.utils.public_utils import Requests
from flask_babel import  gettext as _
from mysite.utils.logger import error_log as logerror
from mysite.utils.public_utils import clear_user_cookie


class CopInfo(Resource):

    def get(self):
        try:
            if g.user:
                username = g.user.username
            else:
                logerror.error("session:%s;errmsg:g.user Not Found"%str(session))
                clear_user_cookie(session)
                return jsonify({"code": 40001, "msg": _("user not login")})

            url = "%s/api/tag/get_taglist_plus/" % current_app.config.get("URL","")
            if username in current_app.config.get("ADMINLIET",[]):
                userType = "superadmin"
            else:
                userType = "admin"

            params = {"user": username, "userType": userType}

            res,data,msg = Requests(url=url,method="GET",params=params)
            if res:
                return jsonify({"code": 20000, "msg": _("success"),"data":data["data"]})
            else:
                return jsonify({"code": 40004, "msg": msg})
        except Exception,e:
            logerror.error("session:%s;errmsg:%s" % (str(session), e))
            clear_user_cookie(session)
            return jsonify({"code": 40001, "msg": _("user not login")})

api.add_resource(CopInfo, "/auth/copInfo")