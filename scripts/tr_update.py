#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/3/15
# @Author  : wangmengyu
# @File    : tr_update.py
# @Software: PyCharm


import os
import sys

if sys.platform == 'win32':
    pybabel = 'env\\Scripts\\pybabel'
else:
    pybabel = 'env/bin/pybabel'
    
os.system(pybabel + ' extract -F babel.cfg -k lazy_gettext -o messages.pot mysite')
os.system(pybabel + ' update -i messages.pot -d mysite/translations')
os.unlink('messages.pot')