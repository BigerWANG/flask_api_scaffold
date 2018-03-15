#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/3/1 16:09
# @Author  : wangmengyu
# @File    : __init__.py.py
# @Software: PyCharm

from mysite.config import CMDB_URL
from mysite.utils.public_utils import Requests

def getDeviceInfo(tag):
    url = "%s/api/device/get_device_list/" % CMDB_URL
    return Requests(url=url, method="GET", params={"tag": tag,"ip_name":"ip"})