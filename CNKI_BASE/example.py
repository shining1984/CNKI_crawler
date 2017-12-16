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
'''��½��ҳ����ȡ��ҳ'''
hosturl='http://www.cnki.net/'
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
magazine='����ѧ��'.decode('gbk').encode('utf8')
txt='����'.decode('gbk').encode('utf8')
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
#���ҳ���Ƿ�����֤��ҳ����ߴ���ҳ��
soup = BeautifulSoup(html2,"html.parser")
contents = []
#��ȡ�����б�
#����б�ҳ�����£���ȡ����url������ֶη���
if soup.find('table', {"class":"GridTableContent"}):
    articles = soup.find('table', {"class":"GridTableContent"}).find_all('tr')
    if articles:
    #ѭ��ץȡ����ҳ,��һ���Ǳ�ͷ����ʹ��
        for index in range(1, len(articles)):
             #ÿƪ���µĻ�����Ϣ�ڲ�ͬ��<td>�У���һ��td�����
             article = articles[index].find_all('td')
             content = {}

             #�������
             content["order"] = article[0].get_text()

             #��������
             if article[1].find('a') and article[1].find('a').get('href'):
                 content["url"] = article[1].find('a').get('href')
             #���������Ӳ����ڣ����ƪ���²�ץȡ
             else:
                 print "WARNING(" + time.strftime("%Y-%m-%d %H:%M:%S") + "):��" + str(content["order"]) + "ƪ����û�����ӣ�������������һƪ"
                 continue
             #���⣬��js�м���
             if article[1].find('script'):
                 s = article[1].find('script').string
                 s = s.replace("document.write(ReplaceChar1(ReplaceChar(ReplaceJiankuohao('", "")
                 s = s.replace("'))));","")
                 s = s.replace("<font class=Mark>","")
                 s = s.replace("</font>","")
                 content["title"] = s

                 #ÿ������λ��һ��<a>��ǩ��
                 content["authors"] = ""
             if article[2].find_all('a'):
                  authors = article[2].find_all('a')
                  for author in authors:
                      #��β����һ���ֺ�
                      content["authors"] += author.get_text() +";"
                 #��Դ�ڿ������
             content["source"] = ""
             if article[3].find("script"):
                 s = article[3].find("script").get_text()
                 k = re.findall(u"[\u4e00-\u9fa5]+\(?[\u4e00-\u9fa5]+\)?",s)
                 if k:
                     content["source"] = k[0]

             #����ʱ��
             content["time"] = ""
             s = article[4].get_text()
             s = s.replace("\r\n","")
             s = s.strip()
             content["time"] = s

             #��Դ���ݿ⣬���ڿ���˶ʿ����ʿ��
             content["db"] = ""
             s = article[5].get_text()
             s = s.replace("\r\n","")
             s = s.strip()
             content["db"] = s

             #��������
             content["cited"] = "0"
             if article[6].find('a'):
                 content["cited"] = article[6].find('a').get_text()

             #���ش���
             content["downloaded"] = "0"
             if article[7].find("span", {"class" : "downloadCount"}):
                 content["downloaded"] = article[7].find("span", {"class" : "downloadCount"}).get_text()
             #����contents�б���
             contents.append(content)
print (repr(contents).decode('unicode-escape'))
file=open('mess','w')
file.write(str(contents))
file.close

