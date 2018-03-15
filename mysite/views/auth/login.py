#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/12/12 19:20
# @Author  : wangmengyu
# @File    : login.py
# @Software: PyCharm

from .. import api
from flask import jsonify, session, g
from flask_restful import Resource, reqparse
from flask_babel import gettext as _
from mysite.utils.ldapbase import ldapserver
from mysite.utils.public_utils import set_user_cookie
from mysite.model import db
from mysite.model.user import User
from mysite.utils.logger import error_log as logerror

parser = reqparse.RequestParser()
parser.add_argument('username', type=unicode, default="")
parser.add_argument('password', type=unicode, default="")


class Login_User(Resource):
    def __init__(self):
        self.ld = ldapserver()
        
    def post(self):
        args = parser.parse_args()
        username = args.get("username")
        password = args.get("password")
        
        if not username or not password:
            return jsonify({"code": 40000, "msg": _("invalid params")})
        try:
            res, data = self.ld.ldap_user_vaild(username, password)
            self.ld.close()
            if not res:
                return jsonify({"code": 40002, "msg": data})
            else:
                user = User.query.filter_by(username=username).first()
                if not user:
                    user = User(
                        username=username,
                        password=password,
                        mobile=data["mobile"],
                        cnname=data["displayName"],
                        userdn=data["userdn"],
                    )
                    db.session.add(user)
                    db.session.commit()
                g.user = user
                set_user_cookie(user,session)
                return jsonify({"code": 20000, "msg": _("success"), "data": {"userName": username}})
        except Exception, e:
            logmsg = "username:%s;errormsg:%s"%e
            logerror.error(logmsg)
            return jsonify({"code": 50000, "msg": _("Internal Server Error")})


api.add_resource(Login_User, "/auth/login")