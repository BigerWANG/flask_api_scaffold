#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/3/1 16:10
# @Author  : wangmengyu
# @File    : agentList.py
# @Software: PyCharm

from . import getDeviceInfo
from .. import api
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_babel import gettext as _
from mysite.config import AGENT_EFFECTIVE_TIME
from mysite.model.device import AgentDevice
from mysite.utils.paginator import pagination_or_not
from mysite.utils.logger import error_log as logerror
import datetime

parser = reqparse.RequestParser()
parser.add_argument('page', type=int, default=1)
parser.add_argument('limit', type=int, default=10)
parser.add_argument('search', type=unicode, default="")
parser.add_argument('ipList', type=unicode, default="", action="append")


class Agent_List(Resource):
    def __init__(self):
        self.foo = lambda s: s['ip']
        
    def _get_info(self, data_list,ipInfo):
        result = []
        for data in data_list:
            ip = data["ip"]
            hostname = data["hostname"]
            version = ""
            status = "STOP"
            if ip in ipInfo:
                uploadTime = ipInfo[ip].get("uploadTime", "")
                version = ipInfo[ip].get("version", "")
                if uploadTime:
                    if uploadTime+datetime.timedelta(seconds=AGENT_EFFECTIVE_TIME) >= datetime.datetime.now():
                        status = "WORKING"
                
            dDict = {
                "hostname": hostname,
                "ip": ip,
                "version": version if version else "-",
                "status": status
            }
            result.append(dDict)
        return result
    
    def get(self, tag=None):
        args = parser.parse_args()
        page = args.get("page")
        limit = args.get("limit")
        search = args.get("search")
        
        if not tag:
            return jsonify({"code": 40000, "msg": _("invalid params")})
        try:
            _d = {
                "total": 0,
                "dataSource": [],
            }
            if search:
                return jsonify({"code": 20000, "msg": "success", "data": _d})
            res, data, msg = getDeviceInfo(tag=tag)
            if not res:
                return jsonify({"code": 40004, "msg": msg, "data": _d})
            
            dataSource = data["data"]
            dataSource.sort(key=self.foo)
            p = pagination_or_not(dataSource, page, limit, sql=False)
            ip_list = [i["ip"] for i in p.object_list]
            AgentDevice_objlist = AgentDevice.query.filter(AgentDevice.ip.in_(ip_list)).all()
            ipInfo  = {}
            for AgentDevice_obj in AgentDevice_objlist:
                ipInfo[AgentDevice_obj.ip] = {
                    "version": AgentDevice_obj.version,
                    "uploadTime": AgentDevice_obj.uploadTime,
                }
            _d["total"] = p.paginator.count
            _d["dataSource"] = self._get_info(p.object_list,ipInfo)
            return jsonify({"code": 20000, "msg": _("success"), "data": _d})
        except Exception, e:
            logmsg = "errormsg:%s" % e
            logerror.error(logmsg)
            return jsonify({"code": 50000, "msg": _("Internal Server Error")})

    def post(self, tag=None):
        args = parser.parse_args()
        ipList = args.get("ipList")
    
        if not tag or not ipList:
            return jsonify({"code": 40000, "msg": _("invalid params")})
        print ipList
        try:
            import time
            time.sleep(3)
            return jsonify({"code": 20000, "msg": "success"})
            
        except Exception, e:
            logmsg = "errormsg:%s" % e
            logerror.error(logmsg)
            return jsonify({"code": 50000, "msg": _("Internal Server Error")})


api.add_resource(Agent_List, "/agent/list/<string:tag>")