# -*- coding: cp936 -*-
import urllib,urllib2,cookielib,httplib,time,re,Parameters

def ToUtf(string):
    return string.decode('gbk').encode('utf8')

class CNKI:
    def search(self):
        #�����������������ҳ,֪����Ҫ���η�������,һ��Ϊ��������,һ��Ϊ����ҳ������
        url='http://epub.cnki.net/KNS/request/SearchHandler.ashx?action=&NaviCode=*&'
        url2='http://epub.cnki.net/kns/brief/brief.aspx?'
        
        #����cookie
        cookie = cookielib.CookieJar()

        #����һ���µ�opener��ʹ��cookiejar
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie),urllib2.HTTPHandler)
        
        #����ͷ�ṹ��ģ�������
        #httplib.HTTPConnection.debuglevel = 1
        hosturl='http://epub.cnki.net/kns/brief/result.aspx?dbprefix=scdb&action=scdbsearch&db_opt=SCDB'
        headers={'Connection':'Keep-Alive',
                 'Accept':'text/html,*/*',
                 'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36',
                 'Referer':hosturl}
        
        #ͨ��chormeץ����ȡ�ύ����,�����ύ������CNKIΪutf-8�������gbk����
        #֪���Ĳ���������UTF8���룬����������Ҫ��gbk�����ٽ���utf-8����
        #�ٽ�����url����,����˳�򲢲�Ӱ���ύ�ɹ�
        parameters=Parameters.parameters()
        postdata=urllib.urlencode(parameters)
        
        #�����ڶ����ύ����������ò����Щ�����Է���ֵû��Ӱ�죬�������޸�keyValue��spvalue��Ȼ����������
        query_string=urllib.urlencode({'pagename':'ASP.brief_result_aspx','DbCatalog':'�й�ѧ��������������ܿ�',
                                       'ConfigFile':'SCDB.xml','research':'off','t':int(time.time()),
                                       'keyValue':'','dbPrefix':'SCDB',
                                       'S':'1','spfield':'SU','spvalue':'',
                                       })
        
        #ʵʩ��һ���ύ����
        req=urllib2.Request(url+postdata,headers=headers)
        html=opener.open(req).read()
        with open('web1.html','w') as e:
            e.write(html)

        #�ڶ����ύ����,�ڶ����ύ��Ľ�����ǲ�ѯ���
        req2=urllib2.Request(url2+query_string,headers=headers)
        result2 = opener.open(req2)
        html2=result2.read()
        #��ӡcookieֵ,�����Ҫ�������µĻ�����Ҫ��½����
        for item in cookie:
            print 'Cookie:%s:/n%s/n'%(item.name,item.value)
        with open('web2.html','w') as e:
            e.write(html2)
        
        #print self.Regular(html)

        #def Regular(self,html):
            #reg='<a href="(.*?)"\ttarget'
            #comlists=re.findall(re.compile(reg),html)
            #return comlists

cnki=CNKI()
cnki.search()
