#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : wang
# @File    : ldapbase.py
# @Software: PyCharm

import ldap
import ldap.async
import string
import ConfigParser
import os


class LdapServer():
    _error = None

    def __init__(self, auto=True):
        self.smap = {"base": ldap.SCOPE_BASE, "onelevel": ldap.SCOPE_ONELEVEL, "subtree": ldap.SCOPE_SUBTREE}

        cf = ConfigParser.ConfigParser()
        if  not os.path.exists("ldap.cfg"):
            cf.add_section("ldap")
            cf.set("ldap","server","ldap://xxx.xxx.com")
            cf.set("ldap","user","xxxx")
            cf.set("ldap","password","xxx")
            cf.set("ldap","xxx","OU=xxx,DC=xxx,DC=com")
            cf.write(open("ldap.cfg", "w"))

        cf.read("ldap.cfg")
        self.conf = cf

        self.ld = None
        if auto:
            self.ld = self.connect()


    @property
    def server(self):
        """当前连接的ldap服务器地址"""
        return self.conf.get('ldap', 'server')

    @property
    def identity(self):
        """当前ldap认证的用户"""
        return self.conf.get('ldap', 'user')

    @property
    def password(self):
        """当前ldap服务认证的密码"""
        return self.conf.get('ldap', 'password')

    @property
    def rootdn(self):
        """当前连接ldap服务器的根节点"""
        return self.conf.get('ldap', 'rootdn')

    def connect(self):
        try:
            self.connection = ldap.initialize(self.server)
            if len(self.identity) > 0:
                # self.connection.simple_bind(self.identity, self.password)
                self.connection.bind_s(self.identity, self.password)
            if self._error:
                self._error = None
        except ldap.LDAPError, e:
            e = dict(e[0])
            self._error = e['desc']
        return self.connection

    def close(self):
        """为了方便使用，只进行默认初始化连接服务器，没有进行自动关闭连接，

        需在每次操作结束后，手动关闭连接
        """
        self.connection.unbind_s()

    def show(self, dn):
        """查看单个ldap信息，只查看该dn的所有属性值"""
        try:
            ldap_result_id = self.ld.search(dn, ldap.SCOPE_SUBTREE, "(objectClass=*)", None)
            result_type, result_data = self.ld.result(ldap_result_id, 0)
            if not result_data:
                return (False, "没有查询到符合条件的结果")
            objattr = result_data[0][1]
            for k in objattr.keys():
                objattr[k] = string.join(objattr[k], ',')
            res = objattr
        except ldap.LDAPError, e:
            return (False, "Failure : Ldap operation failed %s" % str(e))
        return (True, res)

    def search(self, dn, filterstr, s="onelevel"):
        """根据dn的值，进行搜索该dn下的所有符合filterstr的信息

        filterstr符合  `RFC 4515 规范` 一般使用 `(cn=Tom)` 或者 `(objectClass=*)`

        s是搜索方式，默认为onelevel搜索下一级节点，base是搜索当前节点，subtree是搜索下级所有节点包括子节点中的信息

        如果查询过程中不知道用户的rootdn，使用ldapserver.rootdn
        """
        try:
            ldap_result_list = self.ld.search_s(dn, self.smap[s], filterstr)
            if not ldap_result_list:
                return (False, "没有查询到符合条件的结果")
            res = []
            for result in ldap_result_list:
                objattr = result[1]
                for k in objattr.keys():
                    objattr[k] = string.join(objattr[k], ',')
                res.append(objattr)
        except ldap.LDAPError, e:
            return (False, "Failure : Ldap operation search failed %s" % str(e))
        return (True, res)

    def search_s(self, dn, filterstr, s="onelevel"):
        try:
            s_obj = ldap.async.List(
                ldap.initialize('ldap://%s' % self.server),
            )
            s_obj.startSearch(
                dn,
                self.smap[s],
                filterstr
            )
            s_obj.processResults()
            partial = s_obj.allResults
            res = []
            for i in partial:
                r = i[1][1]
                for tmp in r.keys():
                    r[tmp] = string.join(r[tmp], ',')
                res.append(r)
        except ldap.SIZELIMIT_EXCEEDED, e:
            return (False, "Failure : Ldap operation search failed %s" % str(e))
        except ldap.NO_SUCH_OBJECT, e:
            return (False, "Failure : Ldap operation search failed %s" % str(e))
        if res:
            return (True, res)
        else:
            return (False, "No results")
    def ldap_user_vaild(self,username=None,passwd=None):
        filterPattern = "(&(objectClass=person)(sAMAccountName=%s))"%username
        res = self.search(self.rootdn,filterPattern,"subtree")
        if res[0]:
            userdn = res[1][0].get("distinguishedName", "")
            displayName = res[1][0].get("displayName", "")
            mobile = res[1][0].get("mobile", "")
            try:
                if self.ld.bind_s(userdn, passwd):
                    dDict = {
                        "userdn":userdn,
                        "displayName":displayName,
                        "mobile":mobile,
                    }
                    return (True, dDict)
                else:
                    return (False, u"Password ERROR")
            except ldap.LDAPError,e:
                return (False,u"Password ERROR")
        return (False,u"Not Find This User")

if __name__ == "__main__":
    pass
