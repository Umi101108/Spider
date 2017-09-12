# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


class Xianyu(object):

	def __init__(self):
		self.user_url = "https://s.2.taobao.com/list/list.htm?spm=2007.1000337.18.6.80194d2372r4a&usernick=hzy_975"
		self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
		self.headers = {'User-Agent': self.user_agent}

	def getItem(self):
		html = requests.get(self.user_url, headers=self.headers).text
		soup = BeautifulSoup(html, 'lxml')
		item_list = soup.select('.item-info')
		for item in item_list:
			href = 'https:' + item.a.get('href', '')
			title = item.a.get('title')
			desc = item.select('.item-brief-desc')[0].get_text()
			pub_time =  item.select('.item-pub-time')[0].get_text()
			location = item.select('.item-location')[0].get_text()
			print href, title, desc, pub_time, location



if __name__ == "__main__":
	xianyu = Xianyu()
	xianyu.getItem()