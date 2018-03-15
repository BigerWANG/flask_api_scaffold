#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : wangmengyu
# @File    : logger.py
# @Software: PyCharm

import os
from logging.handlers import TimedRotatingFileHandler
from mysite import config
import logging

logging.basicConfig(
        format='%(asctime)s\t%(levelname)s\t%(filename)s\t[line:%(lineno)d] [func:%(funcName)s] [msg:%(message)s]',
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG if config.DEBUG else logging.INFO)

logger_format = '[%(asctime)s][%(thread)d][%(levelname)s][%(filename)s][line:%(lineno)d] [func:%(funcName)s] [msg:%(message)s]'
formatter = logging.Formatter(logger_format)


def get_logger(logger_name, logger_module):
    log_dir = "%s/unknown/" % (config.LOG_DIR)
    if logger_module:
        log_dir = "%s/%s/" % (config.LOG_DIR, logger_module)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log = logging.getLogger(logger_name)
    file_handler = TimedRotatingFileHandler("%s/%s.log" % (log_dir, logger_name), 'W0')
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
    return log

# log
error_log = get_logger("error", "common")
info_log = get_logger("info", "common")
db_log = get_logger("db", "db")
