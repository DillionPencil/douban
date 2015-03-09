#coding=utf-8

import urllib2

import urllib

import cookielib

import time

from bs4 import BeautifulSoup

 

proxy_support = urllib2.ProxyHandler({'http':'http://127.0.0.1:8087'})

opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)

urllib2.install_opener(opener)

while True:
    
    time.sleep(3)
    print '*********testing**********'
