#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : wangmengyu
# @File    : public_utils.py
# @Software: PyCharm

from mysite import config
from flask import g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired,BadSignature
from mysite.model.user import User
from mysite.utils.logger import error_log as logerror
import requests


def set_user_cookie(user, session_):
    if not user:
        return None
    session_[config.SITE_COOKIE] = user.generate_auth_token()


def clear_user_cookie(session_):
    session_[config.SITE_COOKIE] = ""


def get_usertoken_from_session(session_):
    if config.SITE_COOKIE in session_:
        cookies = session_[config.SITE_COOKIE]
        if not cookies:
            logerror.error("session_:%s;key:%s;" % (str(session_), config.SITE_COOKIE))
            return None

        s = Serializer(config.SECRET_KEY)
        try:
            data = s.loads(cookies)
            try:
                user = User.query.get(data['id'])
                g.user = user
                return user
            except Exception,e:
                logerror.error("data:%s;errmsg:%s;"%(str(data),e))
                return None
        except Exception,e:
            logerror.error("data:%s;errmsg:%s;" % (str(s), e))
            return None
        
# 连接第三方系统
def Requests(url="", method="POST", params={}, timeout=20):
    try:
        if method.lower() == "get":
            res = requests.get(url=url, params=params, timeout=timeout)
        else:
            res = requests.post(url=url, data=params, timeout=timeout)
        result = res.json()
        if result["code"] == 200 or result["code"] == 20000:
            return (True, result, "success")
        else:
            return (False, {}, result.get("message", result.get("msg", "Failure")))
    except Exception, e:
        return (False, {}, e)