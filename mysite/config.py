#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : wang
# @File    : config.py
# @Software: PyCharm

import os

# -- app config --
APP_PORT = 8084
DEBUG = True
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYSTEM_TITLE = u"flask scaffold"
PERMANENT_SESSION_LIFETIME = 30 * 24 * 60 * 60
SITE_COOKIE = "My-Agent-ck"
RESTFUL_API_VERSION = "v1"
#单位为秒
AGENT_EFFECTIVE_TIME = 300

# -- flask SECRET_KEY --
# SECRET_KEY = os.urandom(24)
SECRET_KEY = '\xe1\x05\x893x\xf5{\xcfD=\xb1\\\xff4|\x07\xf7\xb8\xda\xc8\xf4<\x8fQ'

# jsonify返回结果不自动排序
# JSON_SORT_KEYS = False

# -- mysql config --
DB_NAME = "agent"
DB_PORT = 3306
MASTER_DB_HOST = "127.0.0.1"
MASTER_DB_HOST_MAX_RETRY_TIMES = 1
MASTER_DB_USER = "root"
MASTER_DB_PASSWD = ""

SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s?charset=utf8" % (MASTER_DB_USER,MASTER_DB_PASSWD,MASTER_DB_HOST,DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_POOL_RECYCLE = 60


# -- LOG DIR --
# LOG_DIR = "%s/log" % ROOT_DIR
LOG_DIR = "/data/plus/systemlog"

# i18n
BABEL_DEFAULT_LOCALE   = 'zh_CN'
BABEL_DEFAULT_TIMEZONE = 'Asia/Shanghai'
# aviliable translations
LANGUAGES   = {
    'en':  'English',
    'zh_CN':  'Chinese-Simplified',
}

URL = "xxx"

# Permission
ADMINLIET = []
