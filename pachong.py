# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import HTMLParser
import urlparse
import urllib
import urllib2
import cookielib
import string
import re
import time
from PIL import Image
from bs4 import BeautifulSoup

proxy_support = urllib2.ProxyHandler({'http':'http://127.0.0.1:8087'})

cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(proxy_support , cookie_support , urllib2.HTTPHandler)
urllib2.install_opener(opener)

origin_url = 'http://api.douban.com/book/subject/'

for i in range(1000001,1999999):    
    print 'Subject ID: %d' % i 
    # time.sleep(3)
    #if not os.path.exists('./book%d' % i):
    #    os.mkdir('./book%d' % i)
    #os.chdir('./book%d' % i)
    book_data = open('book%d_data.txt' % i , 'w')
    url = origin_url + str(i)
    request = urllib2.Request(url)
    fails = 0
    while True:
        if fails >= 5:
            fails = 0
            print 'Fail in connection. Waiting for next chance.'
            time.sleep(10)
        try:
            response = urllib2.urlopen(request , None , 5)
            text = response.read()
        except:
            fails += 1
            print 'an error occured , trying another request'
        else:
            break

    if text.find('wrong subject id') == -1:
        continue

    soup = BeautifulSoup(text)

    book_data.write('title: %s\n' % soup.find('title').string)
    book_data.write('subject ID: %s\n' % str(i))
    for tag in soup.find_all('db:attribute'):
        name = tag.attrs['name']
        data = tag.string
        book_data.write('%s: %s\n' % (name , data))

    for tag in soup.find_all('link'):
        if tag.attrs['rel'] == ['image']:
            book_data.write('image_url: %s\n' % tag.attrs['href'])

    tags = soup.find_all('db:tag')
    book_data.write('tag_num: %d\n' % len(tags))
    for tag in tags:
        book_data.write('%s: %s\n' % (tag.attrs['name'] , tag.attrs['count']))
        
    print 'Finish subject %d' % i
    
    '''
    for tag in soup.find_all('link'):
        if tag.attrs['rel'] == ['image']:
            imgurl = tag.attrs['href']
            request = urllib2.Request(imgurl)
            response = urllib2.urlopen(request)
            img = response.read()
            with open('book_img.jpg' , 'wb') as f:
                f.write(img)
                f.close()
            break
    os.chdir('../')
    '''
