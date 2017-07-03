# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
import sys
sys.setdefaultencoding = 'utf8'

class Douban(object):

	def __init__(self):
		self.base_url = 'https://www.douban.com/group/{}/discussion?start={}'
		self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
		self.headers = {'User-Agent': self.user_agent}

	def getInfo(self, url):
		html = requests.get(url, headers=self.headers).content
		soup = BeautifulSoup(html, 'lxml')
		titles = soup.find('table', class_="olt").find_all('td', class_="title")
		for t in titles:
			title = t.a['title'].strip()
			url = t.a['href'].strip()
			print title, url
			self.getDetail(url)

	def getDetail(self, url):
		html = requests.get(url, headers=self.headers).content
		soup = BeautifulSoup(html, 'lxml')
		content = soup.find('div', class_="topic-doc")
		try:
			print content.text.strip()
		except:
			pass

	def getTotal(self, group):
		for i in range(1, 10, 25):
			self.getInfo(self.base_url.format(group, i))

	def getToCSV(self, title, url, filename='download.csv'):
		with open(filename, 'ab') as csvfile:
			writer = csv.writer(csvfile, dialect = 'excel')
			writer.writerow([title.encode('utf8'), url.encode('utf8')])

if __name__ == "__main__":
	douban = Douban()
	group = 'moeo'
	douban.getTotal(group)

