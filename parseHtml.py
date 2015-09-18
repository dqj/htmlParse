# -*- coding: utf-8 -*-  
#!/usr/bin/python

import sys
import urllib
import re
import json
import time
import glob
import sys
import lxml.html
import codecs
from bs4 import BeautifulSoup
import socket
import os

socket.setdefaulttimeout(10)
reload(sys)
sys.setdefaultencoding("utf-8")

cache = {}
running = True

outputFile = codecs.open("outputInfo.txt","w","utf-8")
# add header
outputFile.write("店名"+'\t'+"星级"+'\t'+"人均消费"+'\t'+"地区"+'\t'+"地址"+'\t'+"电话"+'\t'+"用户点评数量"+'\n')

names = [os.path.basename(x) for x in glob.glob('./*.html')]

starMap = {u'五星商户':'5',u'准五星商户':'4.5',u'四星商户':'4',u'准四星商户':'3.5',u'三星商户':'3',u'准三星商户':'2.5',u'二星商户':'2',u'准二星商户':'1.5',u'一星商户':'1',u'准一星商户':'0.5'}
for fileName in glob.glob('*.html'):
    print fileName
    f = urllib.urlopen(fileName)
    #Thanks to Arturo!
    html = f.read().replace("</html>", "") + "</html>"
    #print html
    soup = BeautifulSoup(html)
    shop_div = {'class':''}
    shopDivs = soup.findAll('dd',attrs = shop_div)
    for shop in shopDivs:
            shopDetail = shop.findAll('ul',{"class":"detail"})
            remark =  shop.findAll('ul',{"class":"remark"})
            if len(shopDetail) > 0 :
                    region = shopDetail[0].findAll('li',{"class":"address"})[0].findAll('a')[0].string
                    shopInfo = shopDetail[0].findAll('li',{"class":"address"})[0].contents[3].split('\n')
                    if len(shopInfo) < 2:
                        print shopInfo
                        telphone = ''
                    else: 
                        telphone = shopInfo[1]
                    address = shopInfo[0]
                    name = shopDetail[0].findAll('a',{"class":"BL"})[0].text
                    price = shop.findAll('strong',{"class":"average"})[0].text
                    if name==None:
                          name = shopDetail[0].findAll('a',{"class":"BL"})[0]['title']  
                    #info = shopDetail.findAll('li',{"class":"shopname"})
                    #price =  shop.findAll('strong',{"class":"average"})
                    #name = info.findAll('a')[0].title
                    star = starMap.get(remark[0].findAll('li')[0].findAll('span')[0]['title'],None)
                    comment = remark[0].findAll('li')[1].findAll('a')[0].string
                    #print #shopDetail[0].findAll('a',{"class":"BL"})[0]['title'] #shopDetail[0].findAll('a',{"class":"BL"})
                    #print name+'\t'+star+'\t'+price+'\t'+region+'\t'+address+'\t'+telphone+'\t'+comment#address.str
                    outputFile.write(name+'\t'+star+'\t'+price+'\t'+region+'\t'+address+'\t'+telphone+'\t'+comment+'\n')
outputFile.close()
