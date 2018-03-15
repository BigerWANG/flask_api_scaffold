#-*- coding:utf-8 -*-

import time

import MySQLdb
import MySQLdb.cursors
from MySQLdb import OperationalError, InternalError

from mysite.utils.logger import db_log as log
from mysite import config

class DB(object):

    def __init__(self, config_):
        self.config = config_
        self._conn = None
        self.host = self.config.MASTER_DB_HOST

    def connect(self, host=None, user=None, passwd=None):
        if not host:
            host = self.host
        if not user:
            user=self.config.MASTER_DB_USER
        if not passwd:
            passwd=self.config.MASTER_DB_PASSWD
        try:
            log.info("conneting [host:%s][user:%s]" % (host, user))
            self._conn and self._conn.close()
            self._conn = MySQLdb.connect(
                host=host,
                port=self.config.DB_PORT,
                user=user,
                passwd=passwd,
                db=self.config.DB_NAME,
                use_unicode=True,
                connect_timeout=5,
                charset="utf8")
            self._conn.autocommit(True)
            log.info("conneted [host:%s][user:%s]" % (host, user))
        except Exception, e:
            log.error("Fatal: connect db fail:%s" % e)
        return self._conn

    def retry(self, *a, **kw):
        cursor = None
        cnt = 0
        while cnt < config.MASTER_DB_HOST_MAX_RETRY_TIMES:
            log.info("begin retry: %s" % cnt)
            time.sleep(2*cnt) #sleep 
            log.info("sleep %s end" % 2*cnt)
            cnt += 1
            try:
                self.connect()
                if not self._conn:
                    continue
                cursor = self._conn.cursor()
                cursor.execute(*a, **kw)
                break
            except (OperationalError, InternalError) as e:
                log.error("Fatal: reconnect db fail:%s" % e)
        log.info("end retried: %s times" % cnt)

        if cursor == None:
            raise Exception("db connection error")
        return cursor

    def execute(self, *a, **kw):
        cursor = None
        try:
            if not self._conn:
                cursor = self.retry(*a, **kw)
            else:
                cursor = self._conn.cursor()
                cursor.execute(*a, **kw)
        except (OperationalError, InternalError) as e:
            log.error("begin retry:%s" % e)
            cursor = self.retry(*a, **kw)

        return cursor

    def close(self):
        if self._conn:
            try:
                cursor = self._conn.cursor()
                if cursor:
                    cursor.close()
            except Exception,e:
                log.debug('close cursor failed')
            self._conn.close()

    def query_all(self, *a, **kw):
        cursor = self.execute(*a, **kw)
        ret = cursor.fetchall()
        cursor and cursor.close()
        return ret

    def insert(self, *a, **kw):
        try:
            cursor = self.execute(*a, **kw)
            id_ = cursor.lastrowid
            cursor and cursor.close()
            return id_
        except:
            return -2

    def update(self, *a, **kw):
        try:
            cursor = self.execute(*a, **kw)
            ret = cursor.rowcount
            cursor and cursor.close()
            return ret
        except:
            return -2

    def delete(self, *a, **kw):
        cursor = self.execute(*a, **kw)
        ret = cursor.rowcount
        cursor and cursor.close()
        return ret

class MixDB():
    def __init__(self):
        self.db_conn = DB(config)

    def insert(self, *a, **kw):
        return self.db_conn.insert(*a, **kw)

    def update(self, *a, **kw):
        return self.db_conn.update(*a, **kw)

    def delete(self, *a, **kw):
        return self.db_conn.delete(*a, **kw)

    def query_all(self, *a, **kw):
        return self.db_conn.query_all(*a, **kw)

    def close(self):
        self.db_conn.close()


class DBQuery(object):
    def __init__(self):
        self.config = config
        self._dtconn = None
        self.host = self.config.MASTER_DB_HOST

    def dtConnect(self, host=None, user=None, passwd=None):
        if not host:
            host = self.host
        if not user:
            user=self.config.MASTER_DB_USER
        if not passwd:
            passwd=self.config.MASTER_DB_PASSWD
        try:
            log.info("conneting [host:%s][user:%s]" % (host, user))
            self._dtconn and self._dtconn.close()
            self._dtconn = MySQLdb.connect(
                host=host,
                port=self.config.DB_PORT,
                user=user,
                passwd=passwd,
                db=self.config.DB_NAME,
                use_unicode=True,
                connect_timeout=5,
                charset="utf8",
                cursorclass = MySQLdb.cursors.DictCursor)
            self._dtconn.autocommit(True)
            log.info("dtConnect conneted [host:%s][user:%s]" % (host, user))
        except Exception, e:
            log.error("Fatal: dtConnect connect db fail:%s" % e)
        return self._dtconn

    def retry(self, *a, **kw):
        cursor = None
        cnt = 0
        while cnt < config.MASTER_DB_HOST_MAX_RETRY_TIMES:
            log.info("DBQuery begin retry: %s" % cnt)
            time.sleep(2*cnt) #sleep 
            log.info("DBQuery sleep %s end" % 2*cnt)
            cnt += 1
            try:
                self.dtConnect()
                if not self._dtconn:
                    continue
                cursor = self._dtconn.cursor()
                cursor.execute(*a, **kw)
                break
            except (OperationalError, InternalError) as e:
                log.error("Fatal: DBQuery reconnect db fail:%s" % e)
        log.info("DBQuery end retried: %s times" % cnt)

        if cursor == None:
            raise Exception("db connection error")
        return cursor

    def execute(self, *a, **kw):
        cursor = None
        try:
            if not self._dtconn:
                cursor = self.retry(*a, **kw)
            else:
                cursor = self._dtconn.cursor()
                cursor.execute(*a, **kw)
        except (OperationalError, InternalError) as e:
            log.error("DBQuery begin retry:%s" % e)
            cursor = self.retry(*a, **kw)

        return cursor

    def close(self):
        if self._dtconn:
            try:
                cursor = self._dtconn.cursor()
                if cursor:
                    cursor.close()
            except Exception,e:
                log.debug('close cursor failed')
            self._dtconn.close()

    def query_all(self, *a, **kw):
        cursor = self.execute(*a, **kw)
        ret = cursor.fetchall()
        cursor and cursor.close()
        return ret
