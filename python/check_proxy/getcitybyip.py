#!/usr/bin/python
#coding:utf-8
# redis queue cache store test


import os
import time
import sys
import urllib



def GetCityByIp(ip):
  ret = ""
  GET_CITY_URL = "http://g1-com-web-01:15426/fcgi/ip2city/query?act=ip2city&ip=%s"
  url = GET_CITY_URL % ip
  response = urllib.urlopen(url).read()
  ret_list =  response.split("\t")
  if len(ret_list) == 10:
    ret = ret_list[7]
  return ret

if __name__ == '__main__':
  print GetCityByIp('202.113.13.168')
  print GetCityByIp('77.94.243.33')
