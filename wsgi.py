#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/3/15
# @Author  : wangmengyu
# @File    : wsgi.py
# @Software: PyCharm

from mysite import app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=app.config.get("APP_PORT", True), debug=app.config.get("DEBUG", True))
