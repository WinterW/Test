#!/usr/bin/env python
# coding=utf-8

import urllib
#import logging
from common import *
proxy_seed_url = ["http://183.131.83.251:888/API?orderid=865319184290474&num=%d&gq=0&carrier=0&protocol=2&an_ha=2&sec=0&zf=0"
                  , "http://183.131.83.251:888/API?orderid=865319184290474&num=%d&gq=0&carrier=0&protocol=2&an_ha=3&sec=0&zf=0"]
#advance_annoymous_proxy_api = "http://183.131.83.251:888/API?orderid=865319184290474&num=%d&gq=0&carrier=0&protocol=2&an_ha=3&sec=0&zf=0"
#annoymous_proxy_api = "http://183.131.83.251:888/API?orderid=865319184290474&num=2000&gq=0&carrier=0&protocol=2&an_ha=3&sec=0&zf=0"

class CGetProxy:
    def __init__(self):
        self.isWriteToFile = 0
        self.proxy_file = 'proxy.txt'

    def setWriteToFileFlag(self, flag):
        self.isWriteToFile = flag

    def getProxyFromUrl(self, proxy_num, proxy_api_url_list):
        #proxy_seed_url = proxy_api_url % (proxy_num)
        remain_num = proxy_num
        proxy_list_total = []
        for proxy_api_url in proxy_api_url_list:
            proxy_seed_url = proxy_api_url % (remain_num)
            try:
                proxy_str =  urllib.urlopen(proxy_seed_url).read()
                proxy_list = proxy_str.strip().split('\r\n')
                proxy_list_total.extend(proxy_list)
            except Exception as ex:
                logging.error('Get proxy failed:[%s].' % (ex))
                return None
                
            if self.isWriteToFile:
                try:
                    of = open(self.proxy_file, 'a+')
                    of.write(proxy_str)
                    of.flush()
                    of.close()
                except Exception as ex:
                    logging.error('write proxy to file failed:[%s].' (ex))
                    return None
            
            remain_num = proxy_num - len(proxy_list_total)
            if remain_num < 0:
                break
        logging.info('Get proxy success, proxy num[%d].' % (len(proxy_list_total)))

        return proxy_list

if __name__ == '__main__':
    proxy_downloader = CGetProxy()
    print proxy_downloader.getProxyFromUrl(100, proxy_seed_url)
    
