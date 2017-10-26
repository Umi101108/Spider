# coding: utf8
import requests
import re

url = 'http://qy1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=25&tableName=TABLE25&tableView=%B9%FA%B2%FA%D2%A9%C6%B7&Id=29813'

response = requests.get(url)
html = response.content
results = re.findall('<tr>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?</tr>', html, re.S)
a = {}
for r in results:
	a[r[0]] = r[1]

for k, v in a.iteritems():
	print k, re.sub('<.*?>', '', v)