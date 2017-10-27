# coding: utf8
import requests
import re
import json
import pprint
import codecs

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9028'
response = requests.get(url, verify=False)
station = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.content.decode('utf8'))
result = json.dumps(dict(station), indent=4).decode('raw_unicode_escape')
with codecs.open('station.py', 'w', encoding='utf8') as pyfile:
	pyfile.write('# coding: utf8\n')
	pyfile.write('station = ')
	pyfile.writelines(result)