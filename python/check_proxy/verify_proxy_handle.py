#!/usr/bin/env python
# coding=utf-8

import datetime
from common import *
from config import *
import db_proxy_handler
import proxy_get
import proxy_check 
from thread_pool import *
import threading
#from Queue import Queue
class CProxyHandle():
    def __init__(self):
        self.m_getProxyHandler = proxy_get.CGetProxy()
        self.m_checkProxyHandler = proxy_check.CCheckProxy()
        self.m_checkProxyHandler.setCheckProxyIp(SHOW_IP_URL)
        self.m_checkProxyHandler.setTimeOut(CHECK_TIMEOUT)
        self.m_dbProxyHandler = db_proxy_handler.CProxyDB() 
        
        #self.validResultList = []
        #self.invalidResultList = []
        self.result_list = []
        self.validProxyLen = 0
        self.rlock = threading.Lock()
        self.wlock = threading.Lock()

        #self.reqTaskQueue = Queue(0)
        #self.rspTaskQueue = Queue(0)
        pass
    def __taskHandle(self, proxy_list):
        #get proxy to check 
        self.rlock.acquire()
        try:
            if len(proxy_list) != 0:
                proxy = proxy_list.pop()
            else:
                logging.info("Proxy list need to be checked is empty, stop all threads.")
                self.thread_pool.stop()
                return 0
        except Exception as ex:#多线程可能存在前面判断proxy_list不空，但执行到此处时，元素已被其它线程取走的情况
            logging.warning("Get proxy from proxy_list failed, error[%s]." % ex)
        finally:
            self.rlock.release()
        proxy_status = self.m_checkProxyHandler.checkProxy(proxy)            
            
        self.wlock.acquire()
        try:
            if PROXY_AVAILABLE == proxy_status:
                self.result_list.append((proxy, VALID, datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
                self.validProxyLen += 1
            else:
                self.result_list.append((proxy, INVALID, datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        except Exception as ex:
            logging.warning("Add proxy into result failed, error[%s]." % ex)
        finally:
            self.wlock.release()
        return 0
    
    def checkProxyList_MT(self, proxy_list):
        checkProxy_worker = worker(self.__taskHandle, proxy_list)
        self.thread_pool = threadPool(CHECK_THREAD_NUM, checkProxy_worker)
        self.thread_pool.start()
        self.thread_pool.join()

    def checkProxyList(self, proxy_list):
        for i in range(len(proxy_list)):
            if PROXY_AVAILABLE == self.m_checkProxyHandler.checkProxy(proxy_list[i]):
                self.result_list.append((proxy_list[i], VALID, datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
                self.validProxyLen += 1
            else:
                self.result_list.append((proxy_list[i], INVALID, datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        
    def proxyHandle(self):
        #check proxy in db
        logging.info("\n\r<===================Check proxy in db================================>")
        proxy_list = self.m_dbProxyHandler.getProxyFromDB(g_db)
        if None != proxy_list:
            self.checkProxyList_MT(proxy_list)
       
        #get and check proxy from url
        logging.info("\n\r<===================Get and check proxy from proxy pool==============>")
        if self.validProxyLen < FIXED_PROXY_NUM:
            proxy_num = (FIXED_PROXY_NUM - self.validProxyLen) << 1
            proxy_list = self.m_getProxyHandler.getProxyFromUrl(proxy_num, PROXY_SEED_URL_LIST)
            if None != proxy_list:
                self.checkProxyList_MT(proxy_list)
        
        #save proxy info to db
        logging.info("\n\r<===================Save proxy info to db============================>")
        self.m_dbProxyHandler.saveResultIntoDB(g_db, self.result_list)

        #delete invalid proxy info in db
        self.m_dbProxyHandler.clearInvalidResult(g_db)

if __name__ == '__main__':
    proxy_handler = CProxyHandle()
    start_time = datetime.datetime.now()
    proxy_handler.proxyHandle()
    end_time = datetime.datetime.now()
    interval = (end_time - start_time).seconds
    logging.info("Proxy check interval:%d, check thread num:%d." % (interval, CHECK_THREAD_NUM))


            

