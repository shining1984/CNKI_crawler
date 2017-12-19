#coding:utf-8
'''
Created on 2016-8-15

@author: 刘帅
'''
import urllib2
from bs4 import BeautifulSoup
import socket
import httplib

urls = []
class Spider3(object):

    def __init__(self, url):
        self.url = url

    def getInfo(self):
        titles = []
        alltime = []
        positions = []
        hdr = {

               'Referer':'http://epub.cnki.net/kns/brief/brief.aspx?curpage=1&RecordsPerPage=20&QueryID=414&ID=&turnpage=1&tpagemode=L&dbPrefix=CJFQ&Fields=&DisplayMode=listmode&PageName=ASP.brief_result_aspx#J_ORDER',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
               'Host':'kc.cnki.net',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        #'Accept-Encoding': 'gzip', 'deflate'
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Request-Line':'http://epub.cnki.net/kns/brief/brief.aspx?curpage=1&RecordsPerPage=20&QueryID=414&ID=&turnpage=1&tpagemode=L&dbPrefix=CJFQ&Fields=&DisplayMode=listmode&PageName=ASP.brief_result_aspx#J_ORDER',
        #'Cookie':'SID=201105'
        'Cookie':'Ecp_ClientId=1160610122903551177; kc_cnki_net_uid=af1af3ce-6313-a666-581e-d71f49479538; RsPerPage=20; ASP.NET_SessionId=d0olsbgo3d0v3kyukigkysl0; Ecp_IpLoginFail=161219118.122.91.183'
        }
        request = urllib2.Request(self.url,headers=hdr)
        page = urllib2.urlopen(request)
        data = page.read()
        #print data
        #request.add_header(hdr)
        try:
            html = urllib2.urlopen(request)
            #print html
        except socket.timeout, e:
            pass
        except urllib2.URLError,ee:
            pass
        except httplib.BadStatusLine:
            pass

        soup = BeautifulSoup(html,'html.parser')
        #print soup
        for link in soup.find_all('a',{'class': 'fz14'}): 
                url = link.get('href').replace('/kns','http://www.cnki.net/KCMS')
                print(url)
                urls.append(link.get('href'))
        #print time
        #time = time_position.split(u'举')[0]
        #position = time_position.split(u'举')[1]
        #print position
        return urls


for i in range(10,13):
    #print i
    url = "http://epub.cnki.net/kns/brief/brief.aspx?curpage=" + str(i) + "&RecordsPerPage=20&QueryID=414&ID=&turnpage=1&tpagemode=L&dbPrefix=CJFQ&Fields=&DisplayMode=listmode&PageName=ASP.brief_result_aspx#J_ORDER"
    #url2 = "http://www.cnena.com/huiyi/list-htm-fid-5-page-" + str(i) + ".html"
    #print url
    s = Spider3(url)
    urls = s.getInfo()
    #urls.extend(url)
print urls
