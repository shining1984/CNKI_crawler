# -*- coding: cp936 -*-
#SU����,TIƪ��,KY�ؼ���,ABժҪ,FTȫ��
#ͨ��chormeץ����ȡ�ύ����,�����ύ������CNKIΪutf-8�������gbk����
#֪���Ĳ���������UTF8���룬����������Ҫ��gbk�����ٽ���utf-8����
import time

def ToUtf(string):
    return string.decode('gbk').encode('utf8')

search={'SU':'','TI':''}
DbCatalog=ToUtf('�й�ѧ��������������ܿ�')
magazine=ToUtf('��ʷ�о�')
times=time.strftime('%a %b %d %Y %H:%M:%S')+' GMT+0800 (�й���׼ʱ��)'

parameter={'ua':'1.21',
            'PageName':'ASP.brief_result_aspx',
            'DbPrefix':'SCDB',
            'DbCatalog':DbCatalog,
            'ConfigFile':'SCDB.xml',
            'db_opt':'CJFQ,CJFN,CDFD,CMFD,CPFD,IPFD,CCND,CCJD,HBRD',
            'base_special1':'%',
            'magazine_value1':magazine,
            'magazine_special1':'%',
            'his':'0',
            '__':times}

def BuildQuery(value):
    par={'txt_1_relation':'#CNKI_AND','txt_1_special1':'='}
    i=0
    for v in value:
        i=i+1
        par['txt_%d_sel'%i]=v
        par['txt_%d_value1'%i]=ToUtf(value[v])
        par['txt_%d_relation'%i]='#CNKI_AND'
        par['txt_%d_special1'%i]='='
    return par

def parameters():
    parameters=dict(parameter,**BuildQuery(search))
    return parameters
