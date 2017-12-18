# -*- coding: cp936 -*-
#author:ѩ֮��
#---------------------

import HTMLParser
import urlparse
import urllib
import urllib2
import cookielib
import string
import re
import time
import httplib
import Cookie
from bs4 import BeautifulSoup


def readtxt(path):
    url=[]
    with open(path,'r') as txt:
        url=txt.readlines()
    return url

#����cookie
httplib.HTTPConnection.debuglevel = 1
cookie = cookielib.CookieJar()

#����һ���µ�opener��ʹ��cookiejar
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie),urllib2.HTTPHandler)
#post��ַ
posturl='http://epub.cnki.net/kns/brief/result.aspx?dbprefix=scdb&action=scdbsearch&db_opt=SCDB'
#����ͷ�ṹ��ģ�������
headers={'Connection':'Keep-Alive',
         'Accept':'text/html,*/*',
         'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36',
         'Referer':posturl}
#ͨ��chormeץ����ȡpostdata

#֪���Ĳ���������UTF8���룬����������Ҫ��gbk�����ٽ���utf-8����
DbCatalog='�й�ѧ��������������ܿ�'.decode('gbk').encode('utf8')
magazine='��ʷ�о�'.decode('gbk').encode('utf8')
txt=''.decode('gbk').encode('utf8')
times=time.strftime('%a %b %d %Y %H:%M:%S')+' GMT+0800 (�й���׼ʱ��)'
parameters={'ua':'1.21',
            'PageName':'ASP.brief_result_aspx',
            'DbPrefix':'SCDB',
            'DbCatalog':DbCatalog,
            'ConfigFile':'SCDB.xml',
            'db_opt':'CJFQ,CJFN,CDFD,CMFD,CPFD,IPFD,CCND,CCJD,HBRD',
            'base_special1':'%',
            'magazine_value1':magazine,
            'magazine_special1':'%',
            'txt_1_sel':'SU',
            'txt_1_value1':txt,
            'txt_1_relation':'#CNKI_AND',
            'txt_1_special1':'=',
            'his':'0',
            '__':times}
postdata=urllib.urlencode(parameters)

query_string=urllib.urlencode({'pagename':'ASP.brief_result_aspx','DbCatalog':'�й�ѧ��������������ܿ�',
                               'ConfigFile':'SCDB.xml','research':'off','t':int(time.time()),
                               'keyValue':'����','dbPrefix':'SCDB',
                               'S':'1','spfield':'SU','spvalue':'����',
                               })
#��������


url='http://epub.cnki.net/KNS/request/SearchHandler.ashx?action=&NaviCode=*&'
url2='http://epub.cnki.net/kns/brief/brief.aspx?'
#��Ҫ�����ύ����һ���ύ���󣬵ڶ������ؿ��
req=urllib2.Request(url+postdata,headers=headers)
html=opener.open(req).read()


req2=urllib2.Request(url2+query_string,headers=headers)

#print req.get_header(),req.header_items()
#����ҳ����½�ɹ�
result2 = opener.open(req2)

html2=result2.read()

with open('web2.html','w') as e:
    e.write(html2)

def Regular(html):
    reg='<a href="(.*?)"\ttarget'
    comlists=re.findall(re.compile(reg),html)
    return comlists

#t=Regular(html2)
#print html2  

############################################################################################################

soup = BeautifulSoup(html2,"html.parser")
contents = []
for tr in soup.findAll('tr'):
    content = {}
    article = tr.find_all('td')
    if tr.find('a') and tr.find('a').get('href') and tr.find('a').get('target') and article[1].find('script'):

########################################################################################
        #Get the article number
        content["order"] = ""
        content["order"] = article[0].get_text()
        print content["order"]
        #Get the article title
        content["title"] = ""
        s = tr.find('script').string
        s = s.replace("document.write(ReplaceChar1(ReplaceChar(ReplaceJiankuohao('", "")
        s = s.replace("'))));","")
        s = s.replace("<font class=Mark>","")
        s = s.replace("</font>","")
        content["title"] = s
        print content["title"]
        #Get the article authors
        content["authors"] = ""
        if article[2].find_all('a'):
            authors = article[2].find_all('a')
            for author in authors:
                content["authors"] += author.get_text() +";"
        print content["authors"]
        #The org of the article come from
        content["source"] = ""
        if article[3].find("script"):
            s = article[3].find("script").get_text()
            k = re.findall(u"[\u4e00-\u9fa5]+\(?[\u4e00-\u9fa5]+\)?",s)
            if k:
                content["source"] = k[0]
        print content["source"]
        #����ʱ��
        content["time"] = ""
        s = article[4].get_text()
        s = s.replace("\r\n","")
        s = s.strip()
        content["time"] = s
        print content["time"]
        #��Դ���ݿ⣬���ڿ���˶ʿ����ʿ��
        content["db"] = ""
        s = article[5].get_text()
        s = s.replace("\r\n","")
        s = s.strip()
        content["db"] = s
        print content["db"]
        #��������
        content["cited"] = "0"
        if article[6].find('a'):
            content["cited"] = article[6].find('a').get_text()
        print content["cited"]
        #���ش���
        content["downloaded"] = "0"
        if article[7].find("span", {"class" : "downloadCount"}):
            content["downloaded"] = article[7].find("span", {"class" : "downloadCount"}).get_text()
        print content["downloaded"]
        #����contents�б���
        contents.append(content)
######################################################################################
        print "#######################################"
#############################################################################
print contents
