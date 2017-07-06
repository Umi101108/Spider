# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


class Smzdm(object):

	def __init__(self):
		self.base_url = "http://www.smzdm.com/p/1000211/"
		self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
		self.headers = {'User-Agent': self.user_agent}

	def getInfo(self, url):
		html = requests.get(url, headers=self.headers).text
		soup = BeautifulSoup(html, 'lxml')
		comment_listBox = soup.select('ul.comment_listBox')
		comment_list = comment_listBox.select('.comment_list')
		for comment in comment_list:
			print comment


	def main(self):
		self.getInfo(self.base_url)


if __name__ == '__main__':
	smzdm = Smzdm()
	smzdm.main()