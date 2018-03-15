#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/12/8 15:22
# @Author  : wangmengyu
# @File    : __init__.py
# @Software: PyCharm

from flask import Flask, request, g, session, jsonify
from flask_babel import Babel, gettext as _
from mysite import config
from mysite.views import Api_Blueprint
from mysite.model import db
from mysite.utils.public_utils import get_usertoken_from_session
from mysite.utils.logger import error_log as logerror
from mysite.utils.logger import info_log as loginfo

#-- create app --

app = Flask(__name__)
app.config.from_object("mysite.config")
babel = Babel(app)
db.init_app(app)


app.register_blueprint(Api_Blueprint)
# app.app_context().push()

@babel.localeselector
def get_locale():
    return  app.config.get("BABEL_DEFAULT_LOCALE")

@babel.timezoneselector
def get_timezone():
    return app.config.get("BABEL_DEFAULT_TIMEZONE")

    
@app.before_request
def app_before():
    loginfo.info("session:%s"%(str(session)))
    g.user = get_usertoken_from_session(session)
    path = request.path
    if not g.user and not path.endswith("/auth/login"):
        logerror.error("session:%s;errmsg:g.user Not Found" % str(session))
        return jsonify({"code": 40001, "msg": _("user not login")})
    
@app.teardown_appcontext
def shutdown_session(exception=None):
  db.session.close()
