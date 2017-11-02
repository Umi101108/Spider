# coding: utf8
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# driver = webdriver.Chrome("D:\chromedriver_win32\chromedriver.exe")
# driver.get('http://qy1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=25&tableName=TABLE25&tableView=%B9%FA%B2%FA%D2%A9%C6%B7&Id=233')
# elem = driver.find_element_by_xpath('')
# keyword = ''.encode('utf8')
# elem.send_keys(keyword, Keys.RETURN)

# html = driver.page_source
# print html


user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
headers = {'User-Agent': user_agent}
for i in xrange(233, 234):
	url = 'http://qy1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=25&tableName=TABLE25&tableView=%B9%FA%B2%FA%D2%A9%C6%B7&Id={}'.format(str(i))
	response = requests.get(url, headers=headers)
	html = response.content
	print html
# 	# results = re.findall('<tr>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?</tr>', html, re.S)
# 	# a = {}
# 	# for r in results:
# 	# 	a[r[0]] = r[1]
# 	# 	print r

# 	# for k, v in a.iteritems():
# 	# 	print k, re.sub('<.*?>', '', v)