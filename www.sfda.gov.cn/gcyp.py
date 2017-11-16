# coding: utf8
import requests
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
# 更换头部
options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')

driver = webdriver.Chrome("D:\chromedriver_win32\chromedriver.exe", chrome_options=options)
# driver.get('http://qy1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=25&tableName=TABLE25&tableView=%B9%FA%B2%FA%D2%A9%C6%B7&Id=233')
# elem = driver.find_element_by_xpath('')
# keyword = ''.encode('utf8')
# elem.send_keys(keyword, Keys.RETURN)

# html = driver.page_source
# print html


user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
headers = {'User-Agent': user_agent}
url = 'http://qy1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=25&tableName=TABLE25&title=%B9%FA%B2%FA%D2%A9%C6%B7&bcId=124356560303886909015737447882'
driver.get(url)
time.sleep(5)
elem = driver.find_element_by_xpath('//*[@id="keyword"]')
keyword = 'H20056946'.encode('utf8')
elem.send_keys(keyword)
time.sleep(5)
# next_page = driver.find_element_by_xpath('//*[@id="content"]/div/table[4]/tbody/tr/td[4]')
# next_page.click()
# search = driver.find_element_by_xpath('//*[@name="Submit"]')
# search.click()
# time.sleep(5)
print driver.page_source
# for i in xrange(233, 234):
# 	url = 'http://qy1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=25&tableName=TABLE25&tableView=%B9%FA%B2%FA%D2%A9%C6%B7&Id={}'.format(str(i))
# 	response = requests.get(url, headers=headers)
# 	html = response.content
# 	print html
# 	# results = re.findall('<tr>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?</tr>', html, re.S)
# 	# a = {}
# 	# for r in results:
# 	# 	a[r[0]] = r[1]
# 	# 	print r

# 	# for k, v in a.iteritems():
# 	# 	print k, re.sub('<.*?>', '', v)