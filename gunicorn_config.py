#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/3/15
# @Author  : wangmengyu
# @File    : gunicorn_config.py
# @Software: PyCharm

import os
import sys
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import os
import multiprocessing
from mysite.config import APP_PORT, LOG_DIR

bind = '127.0.0.1:%s' % APP_PORT
backlog = 2048
timeout = 30
daemon = True
reload = True
#worker_class = 'gevent'

try:
    workers =  multiprocessing.cpu_count()
except:
    workers = 4
threads = 2

log_path = "%s/gunicorn"%LOG_DIR
try:
    if not os.path.exists(log_path):
        os.makedirs(log_path)
except:pass

loglevel = 'debug'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'

accesslog = "/dev/null"
errorlog = "/dev/null"

acclog = logging.getLogger('gunicorn.access')
acclog.addHandler(WatchedFileHandler('%s/access.log'%log_path))
acclog.propagate = False
errlog = logging.getLogger('gunicorn.error')
errlog.addHandler(WatchedFileHandler('%s/error.log'%log_path))
errlog.propagate = False
