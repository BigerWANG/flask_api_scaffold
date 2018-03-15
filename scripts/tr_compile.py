#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/3/15
# @Author  : wangmengyu
# @File    : tr_compile.py
# @Software: PyCharm


import os
import sys

if sys.platform == 'win32':
    pybabel = 'env\\Scripts\\pybabel'
else:
    pybabel = 'env/bin/pybabel'
    
os.system(pybabel + ' compile -d mysite/translations')
