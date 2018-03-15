#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/3/15
# @Author  : wangmengyu
# @File    : tr_init.py
# @Software: PyCharm


import os
import sys

if sys.platform == 'win32':
    pybabel = 'env\\Scripts\\pybabel'
else:
    pybabel = 'env/bin/pybabel'
if len(sys.argv) != 2:
    print "usage: tr_init <language-code>"
    sys.exit(1)
    
os.system(pybabel +
          ' extract -F babel.cfg -k lazy_gettext -o messages.pot mysite')
os.system(pybabel +
          ' init -i messages.pot -d mysite/translations -l ' + sys.argv[1])
os.unlink('messages.pot')
