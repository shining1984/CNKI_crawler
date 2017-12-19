
zy900406

selenium python的使用(一)

下面是一个爬取知网数据的例子，使用selenium 用python爬取数据

1.创建对象，打开指定地址，在休眠的20秒内输入搜索项

driver= webdriver.Chrome()

driver.get("http://epub.cnki.net/kns/brief/result.aspx?dbprefix=scdb&action=scdbsearch&db_opt=SCDB")

time.sleep(20)
2.点击搜索按钮，休眠5秒，等待渲染结束
driver.find_element_by_id('btnSearch').click()
time.sleep(5)

3.根据选择搜索项，找到key并指定地址（此处和业务有关）

key=driver.find_element_by_id('curdbcode').get_attribute('value').upper()
url='http://epub.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_result_aspx&dbPrefix=[KEY]&ConfigFile=[KEY].xml&recordsperpage=50'.replace('[KEY]', key)
driver.get(url)

#nextPage()方法，是否有下一页，控制翻页操作

nextPage(driver)

def nextPage(driver):

#当前页面的url

urll=driver.current_url
html=driver.page_source.encode('utf8')
if 'TitleLeftCell' in html:

　　#根据class name查找

　　linkss=driver.find_element_by_class_name('TitleLeftCell')
　　if linkss:

　　　　#根据节点name查找
　　　　for link in linkss.find_elements_by_tag_name("a"):
　　　　　　titlevalue=link.text
　　　　　　if titlevalue=='下一页':

　　　　　　　　#模拟点击操作
　　　　　　　　link.click()
　　　　　　　　time.sleep(5)
　　　　　　　　nextPage(driver)
　　　　　　　　break



zy900406

selenium python的使用(二)

1.selenium获取到的信息是 把页面加载完毕之后

获取异步加载的html源码

html=driver.find_element_by_xpath("/html").get_attribute("outerHTML").encode('utf-8')

某个淘宝商品例子

from selenium import webdriver #引用
driver= webdriver.Chrome() #显式打开浏览器
driver.get('https://item.taobao.com/item.htmid=538846883844&ali_refid=a3_430585_1006:1106199306:N:%E8%A2%96%E5%A4%B4:ca6a06e1f2de29945b120e5f9e02b0c2&ali_trackid=1_ca6a06e1f2de29945b120e5f9e02b0c2&spm=a230r.1.14.1.puJ4aY#detail') #跳转到指定页面
html=driver.find_element_by_xpath("/html").get_attribute("outerHTML").encode('utf-8')
print html

获取到的某个html中有此商品价格
