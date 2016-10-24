#!/usr/bin/env python
# coding=utf-8

import urllib2
import re 
from config import *
from common import *
#ERROR CODE
#PROXY_AVAILABLE, PROXY_UNEXPECT, PROXY_UNKNOW_ERR, PROXY_UNAVAILABLE, PROXY_TRANSPARENT = range(5)
#advance_annoymous_proxy_api = "http://183.131.83.251:888/API?orderid=865319184290474&num=2000&gq=0&carrier=0&protocol=2&an_ha=3&sec=0&zf=0"
#annoymous_proxy_api = "http://183.131.83.251:888/API?orderid=865319184290474&num=2000&gq=0&carrier=0&protocol=2&an_ha=3&sec=0&zf=0"

class CCheckProxy:
    def __init__(self):
        self.checkProxyIP = 'www.baidu.com'
        self.timeout = 5 

        pass
    
    def setTimeOut(self, timeout):
        self.timeout = timeout

    def setCheckProxyIp(self, checkProxyIp):
        self.checkProxyIP = checkProxyIp


    def checkProxy(self, proxy):
        #https检测 
        proxy_map = {'https': '%s' % (proxy)}
        handler = urllib2.ProxyHandler(proxy_map)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        
        try:
            f = opener.open(CHECK_HTTPS_URL, timeout = self.timeout)#, None, self.timeout)
           # f = urllib2.urlopen(self.checkProxyIP, None, self.timeout)
        except Exception as ex:
            logging.warning("Proxy %s is unavailable, error[%s]." % (proxy, ex))
            return PROXY_UNAVAILABLE
        if not f or f.code != 200:
            logging.warning("Proxy %s is unavailable. error[return code:%d]." % (proxy, f.code))
            return PROXY_UNAVAILABLE 
         
        #http检测
        proxy_map = {'http': '%s' % (proxy)}
        handler = urllib2.ProxyHandler(proxy_map)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        
        try:
            f = opener.open(self.checkProxyIP, timeout = self.timeout)#, None, self.timeout)
           # f = urllib2.urlopen(self.checkProxyIP, None, self.timeout)
        except Exception as ex:
            logging.warning("Proxy %s is unavailable, error[%s]." % (proxy, ex))
            return PROXY_UNAVAILABLE
        if not f or f.code != 200:
            logging.warning("Proxy %s is unavailable. error[return code:%d]." % (proxy, f.code))
            return PROXY_UNAVAILABLE
        
        ip = proxy.split(':')[0]
        try:
            response = str(f.read())
            if response != str(ip): 
                logging.warning('Proxy %s is unavailable, error[unexpected response:%s].' % (proxy, response))
                return PROXY_UNEXPECT
        #    else:
        #        logging.info('Proxy %s is available.' % (proxy))
        #        return PROXY_AVAILABLE
        except Exception as ex:
            logging.error('Read response of proxy %s  error, error[%s].' % (proxy, ex))
            return PROXY_UNKNOW_ERR
        
        logging.info('Proxy %s is available.' % (proxy))
        return PROXY_AVAILABLE

   
   
if __name__ == '__main__':
  checkProxy = CCheckProxy()
  checkProxy.setTimeOut(10)
  checkProxy.setCheckProxyIp('http://diagtool.ganji.com/showip.php')
  print checkProxy.checkProxy('183.230.53.186:8123')
  print checkProxy.checkProxy('123.129.203.87:80')
  print checkProxy.checkProxy('103.31.7.161:80')

