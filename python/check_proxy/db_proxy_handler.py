#!/usr/bin/env python
# coding=utf-8
import MySQLdb 
import datetime 
from config import *
from common import * 
from getcitybyip import *
class CProxyDB:
    def __init__(self):
        pass
    #get proxy from sql db, only valid
    def getProxyFromDB(self, dbconfig):
        try:
            #connect
            conn = MySQLdb.connect(host = dbconfig['host']
                                   , port = dbconfig['port']
                                   , db = dbconfig['db']
                                   , user=dbconfig['user']
                                   , passwd=dbconfig['passwd']
                                   , charset="utf8")
            cursor = conn.cursor()

            #search
            sql = "SELECT %s FROM ip_resource WHERE status = 0" % ('ip')
            #param = ("ip")
            n = cursor.execute(sql)#, param)

            #get result
            result_list = cursor.fetchall()
        except Exception as ex:
            result_list = None
            logging.error('Get proxy from db failed, error:[%s]', ex)
            return None
        finally:
            cursor.close()
            conn.close()

        proxy_list = []
        for i in range(len(result_list)):
            proxy_list.append(result_list[i][0])
        return proxy_list
    #save and update proxy info in sql db, valid/invalid need to be update 
    def saveResultIntoDB(self, dbconfig, proxy_list):
        #connect
        try:
            conn = MySQLdb.connect(host = dbconfig['host']
                                   , port = dbconfig['port']
                                   , db = dbconfig['db']
                                   , user=dbconfig['user']
                                   , passwd=dbconfig['passwd']
                                   , charset="utf8")
            cursor = conn.cursor()
        except Exception as ex:
            logging.error("Connect db[host:%s, db:%s] failed, error[%s]" %  (dbconfig['host'], dbconfig['db'], ex))
            return -1 
      
        #search
        sql = 'INSERT INTO ip_resource (city, ip, location, create_time, status, proxyid, upperlimit) VALUES(%s, %s, %s, %s, %s, %s, 50000) ON DUPLICATE KEY UPDATE location=%s, status=%s'
        param_list = []
        for proxy in proxy_list:
            status = proxy[STATUS]
            ip = proxy[PROXY].split(":")[0]
            location = GetCityByIp(ip)
            #if status == 0:
            param_list.append(("lasa"
                              , proxy[PROXY]
                              , location 
                              , datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                              , status
                              , 'pubproxy_%s' % (proxy[PROXY])
                              , location 
                              , status
                              ))

        #insert/update
        try:
            n = cursor.executemany(sql, param_list)
            conn.commit()
        except Exception as ex:
            logging.error("Insert/Update db[host:%s, db:%s] failed, error[%s]" % (dbconfig['host'], dbconfig['db'], ex))
            return -1
        if n != None:
            logging.info('Save %d proxy into db[host:%s, db:%s]' %  (n, dbconfig['host'], dbconfig['db']))
        else:
            logging.warning('No new proxy status update.')
        return 0

    def clearInvalidResult(self, dbconfig):
        #connect
        try:
            conn = MySQLdb.connect(host = dbconfig['host']
                                   , port = dbconfig['port']
                                   , db = dbconfig['db']
                                   , user=dbconfig['user']
                                   , passwd=dbconfig['passwd']
                                   , charset="utf8")
            cursor = conn.cursor()
        except Exception as ex:
            logging.error("Connect db[host:%s, db:%s] failed, error[%s]" % (dbconfig['host'], dbconfig['db'], ex))
            return -1 
      
        #search
        sql = "delete from ip_resource where status = 1"
        
        #insert/update
        try:
            n = cursor.execute(sql)
            conn.commit()
        except Exception as ex:
            logging.error("Delete invalid from db[host:%s, db:%s] failed, error[%s]" % (dbconfig['host'], dbconfig['db'], ex))
            return -1
        logging.info('Delete %d invalid proxy from db[host:%s, db:%s]' % (n, dbconfig['host'], dbconfig['db']))
