# -*- coding: utf-8 -*-

import time
import requests
import json

# 实际request_url如下，数字分别表示年份、地点、年月、unix时间戳
example_url = 'http://d1.weather.com.cn/calendar_new/2017/101020100_201706.html?_=1496201031604'

class Weather(object):

	def __init__(self):
		self.base_url = 'http://d1.weather.com.cn/calendar_new/{}/101020100_{}.html'
		self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
		self.referer = 'http://www.weather.com.cn/weather40d/101020100.shtml'
		self.headers = {'User-Agent': self.user_agent, 'Referer': self.referer}
		self.result = []

	def getInfo(self, url):
		html = requests.get(url, headers=self.headers).content.decode(encoding='utf-8')
		data = json.loads(html[11:])
		for i in data:
			print i.get('date'), i.get('hmax'), i.get('hmin'), i.get('hgl'), i.get('fe'), i.get('wk'), i.get('time')
		# key = {'date': '日期', 'hmax': '最高温', 'hmin': '最低温', 'hgl': '湿度', 'fe': '节日', 'wk': '星期', 'time': '时间'}
		# for i in data:
		# 	print {v: i[k] for k, v in key.items()}

	def getUrl(self, year, month):
		y = str(year)
		m = str(month) if month>9 else "0"+str(month)
		url = self.base_url.format(y, y+m)
		return url

if __name__ == "__main__":
	weather = Weather()
	year = 2016
	month = 4 
	url = weather.getUrl(year, month)
	weather.getInfo(url)
