# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class JianShu(object):

	def __init__(self):
		self.url = 'http://www.jianshu.com/trending/weekly?page={}'
		self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
		self.headers = {'User-Agent': self.user_agent}
		self.result = []

	def getInfo(self, url):
		html = requests.get(url, headers=self.headers).text
		# print html
		soup = BeautifulSoup(html, 'lxml')
		notes = soup.find('ul', class_='note-list').find_all('li')
		for note in notes:
			name = note.find('a', class_='blue-link').text
			title = note.find('a', class_='title').text
			url = 'http://www.jianshu.com' + note.find('a', class_='title')['href']
			abstract = note.find('p', class_='abstract').text.strip()
			try:
				tag = note.find('a', class_='collection-tag').text.strip()
			except:
				tag = None
			reads = note.find('i', class_='iconfont ic-list-read').parent.text.strip()
			comments = note.find('i', class_='iconfont ic-list-comments').parent.text.strip()
			likes = note.find('i', class_='iconfont ic-list-like').parent.text.strip()
			try:
				moneys = note.find('i', class_='iconfont ic-list-money').parent.text.strip()
			except:
				moneys = None
			# print name, '【' + title + '】', reads, comments, likes
			# print abstract

			data = {
				"name": name,
				"title": title,
				"url": url,
				"tag": tag,
				"abstract": abstract,
				"reads": reads,
				"comments": comments,
				"likes": likes,
				"moneys": moneys,
			}
			self.result.append(data)
			


	def getTotal(self):
		for i in range(1, 10):
			url = self.url.format(str(i))
			self.getInfo(url)

		for i in self.result:
			print "#"*66 + str(self.result.index(i)+1)
			for k, v in i.iteritems():
				print k, v


if __name__ == '__main__':
	jianshu = JianShu()
	jianshu.getTotal()