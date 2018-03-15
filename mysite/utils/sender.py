#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/12/8 16:32
# @Author  : wangmengyu
# @File    : sender.py
# @Software: PyCharm

from flask.ext.babel import  gettext as _
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mysite.utils.logger import info_log as loginfo
from mysite.utils.logger import error_log as logerror
import smtplib
import ConfigParser
import os


class Sender(object):
    
    def __init__(self):

        cf = ConfigParser.ConfigParser()
        if not os.path.exists("sender.cfg"):
            # Mail config
            cf.add_section("Mail")
            cf.set("Mail", "server", "smtp.qq.com")
            cf.set("Mail", "user", "test@qq.com")
            cf.set("Mail", "password", "*****")
            
            # Sms config
            cf.add_section("Sms")
            cf.set("Sms", "url", "http://www.****.com/api/v1/sender/sms")
            
            cf.write(open("sender.cfg", "w"))

        cf.read("sender.cfg")
        self.conf = cf

    def sendMail(self,tos="",subject="",content="",content_type="plain"):
        try:
            mail_server = self.conf.get('Mail', 'server')
            mail_user = self.conf.get('Mail', 'user')
            mail_password = self.conf.get('Mail', 'password')
            
            if not mail_server or not mail_user or not mail_password:
                errmsg = _("Mailbox configuration error")
                logerror.error("server:%s,user:%s,password:%s,errmsg:%s"%(mail_server,mail_user,mail_password,errmsg))
                return (False, errmsg)
        except Exception,e:
            errmsg = _("Mailbox configuration error")
            logerror.error("errmsg:%s,errinfo:%s" % (errmsg,e))
            return (False, errmsg)
        
        if not tos or not content or not subject:
            errmsg = _("The recipient or the content is empty")
            logerror.error("tos:%s,content:%s,subject:%s,errmsg:%s"% (tos, content, subject, errmsg))
            return (False, errmsg)
        
        server = smtplib.SMTP()
        try:
            server.connect(mail_server, 587)  # 连接服务器
            server.starttls()
            server.login(mail_user, mail_password)  # 登录操作
            to_list = tos.split(",")
            msg = MIMEMultipart('related')
            msgAlternative = MIMEMultipart('alternative')
            msg.attach(msgAlternative)
            msgText = MIMEText(content, content_type, _charset='utf-8')
            msgAlternative.attach(msgText)
            msg['Subject'] = subject
            msg['From'] = mail_user
            msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
            server.sendmail(mail_user, to_list, msg.as_string())
            server.quit()
            loginfo.info("tos:%s,content:%s,subject:%s"% (tos, content, subject))
            return (True, _("success"))
        except Exception, e:
            logerror.error("tos:%s,content:%s,subject:%s,errmsg:%s"% (tos, content, subject,e))
            return (False, "sendMail error:%s" % e)
        
    def sendSms(self,tos="",content=""):
        sms_url = self.conf.get('Sms', 'url')
        if not sms_url:
            errmsg = _("SMS configuration error")
            logerror.error("url:%s,errmsg:%s"% (str(sms_url),errmsg))
            return (False, errmsg)

        if not tos or not content :
            errmsg = _("The recipient or the content is empty")
            logerror.error("tos:%s,content:%s,errmsg:%s"%(tos, content, errmsg))
            return (False, errmsg)
        
        return (False, _("This function is not implemented temporarily"))

if __name__ == '__main__':
    send = Sender()
    res = send.sendMail("test@qq.com","test","test")