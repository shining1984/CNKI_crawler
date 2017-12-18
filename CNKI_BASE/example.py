# -*- coding: cp936 -*-
#author:雪之忆
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
'''登陆网页，读取网页'''
#hosturl='http://www.cnki.net/'
#生成cookie
httplib.HTTPConnection.debuglevel = 1
cookie = cookielib.CookieJar()

#创建一个新的opener来使用cookiejar
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie),urllib2.HTTPHandler)
#post地址
posturl='http://epub.cnki.net/kns/brief/result.aspx?dbprefix=scdb&action=scdbsearch&db_opt=SCDB'
#构建头结构，模拟浏览器
headers={'Connection':'Keep-Alive',
         'Accept':'text/html,*/*',
         'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36',
         'Referer':posturl}
#通过chorme抓包获取postdata

#知网的参数编码是UTF8编码，所以中文需要先gbk解码再进行utf-8编码
DbCatalog='中国学术文献网络出版总库'.decode('gbk').encode('utf8')
magazine='历史研究'.decode('gbk').encode('utf8')
txt=''.decode('gbk').encode('utf8')
times=time.strftime('%a %b %d %Y %H:%M:%S')+' GMT+0800 (中国标准时间)'
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

query_string=urllib.urlencode({'pagename':'ASP.brief_result_aspx','DbCatalog':'中国学术文献网络出版总库',
                               'ConfigFile':'SCDB.xml','research':'off','t':int(time.time()),
                               'keyValue':'隔离','dbPrefix':'SCDB',
                               'S':'1','spfield':'SU','spvalue':'隔离',
                               })
#发送请求


url='http://epub.cnki.net/KNS/request/SearchHandler.ashx?action=&NaviCode=*&'
url2='http://epub.cnki.net/kns/brief/brief.aspx?'
#需要两步提交，第一部提交请求，第二步下载框架
req=urllib2.Request(url+postdata,headers=headers)
html=opener.open(req).read()


req2=urllib2.Request(url2+query_string,headers=headers)

#print req.get_header(),req.header_items()
#打开网页，登陆成功
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
        #发表时间
        content["time"] = ""
        s = article[4].get_text()
        s = s.replace("\r\n","")
        s = s.strip()
        content["time"] = s
        print content["time"]
        #来源数据库，如期刊，硕士，博士等
        content["db"] = ""
        s = article[5].get_text()
        s = s.replace("\r\n","")
        s = s.strip()
        content["db"] = s
        print content["db"]
        #被引次数
        content["cited"] = "0"
        if article[6].find('a'):
            content["cited"] = article[6].find('a').get_text()
        print content["cited"]
        #下载次数
        content["downloaded"] = "0"
        if article[7].find("span", {"class" : "downloadCount"}):
            content["downloaded"] = article[7].find("span", {"class" : "downloadCount"}).get_text()
        print content["downloaded"]
        #存如contents列表里
        contents.append(content)
######################################################################################
        print "#######################################"
#############################################################################
print contents
'''if soup.find('table', {"class":"GridTableContent"}):
    articles = soup.find('table', {"class":"GridTableContent"}).find_all('tr')
    #articles = soup.find('', {"class":""}).find_all('tr')
    print len(articles)
    if articles:
    #循环抓取内容页,第一行是表头，不使用
        for index in range(1, len(articles)):
             #每篇文章的基本信息在不同的<td>中，第一个td是序号
             article = articles[index].find_all('td')
             content = {}

             #文章序号
             content["order"] = article[0].get_text()

             #文章链接
             if article[1].find('a') and article[1].find('a').get('href'):
                 content["url"] = article[1].find('a').get('href')
             #若文章链接不存在，则该篇文章不抓取
             else:
                 print "WARNING(" + time.strftime("%Y-%m-%d %H:%M:%S") + "):第" + str(content["order"]) + "篇文章没有链接，跳过，继续下一篇"
                 continue
             #标题，从js中检索
             if article[1].find('script'):
                 s = article[1].find('script').string
                 s = s.replace("document.write(ReplaceChar1(ReplaceChar(ReplaceJiankuohao('", "")
                 s = s.replace("'))));","")
                 s = s.replace("<font class=Mark>","")
                 s = s.replace("</font>","")
                 content["title"] = s

                 #每个作者位于一个<a>标签内
                 content["authors"] = ""
             if article[2].find_all('a'):
                  authors = article[2].find_all('a')
                  for author in authors:
                      #结尾多了一个分号
                      content["authors"] += author.get_text() +";"
                 #来源期刊或机构
             content["source"] = ""
             if article[3].find("script"):
                 s = article[3].find("script").get_text()
                 k = re.findall(u"[\u4e00-\u9fa5]+\(?[\u4e00-\u9fa5]+\)?",s)
                 if k:
                     content["source"] = k[0]

             #发表时间
             content["time"] = ""
             s = article[4].get_text()
             s = s.replace("\r\n","")
             s = s.strip()
             content["time"] = s

             #来源数据库，如期刊，硕士，博士等
             content["db"] = ""
             s = article[5].get_text()
             s = s.replace("\r\n","")
             s = s.strip()
             content["db"] = s

             #被引次数
             content["cited"] = "0"
             if article[6].find('a'):
                 content["cited"] = article[6].find('a').get_text()

             #下载次数
             content["downloaded"] = "0"
             if article[7].find("span", {"class" : "downloadCount"}):
                 content["downloaded"] = article[7].find("span", {"class" : "downloadCount"}).get_text()
             #存如contents列表里
             contents.append(content)


print (repr(contents).decode('unicode-escape'))'''


