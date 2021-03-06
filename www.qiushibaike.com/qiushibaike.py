# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
import time
import requests
from bs4 import BeautifulSoup


class QiuBai(object):

	def __init__(self):
		self.url = 'http://www.qiushibaike.com/text/'
		self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
		self.headers = {'User-Agent': self.user_agent}

	def getNextUrl(self, url):
		html = requests.get(url, headers=self.headers).text
		soup = BeautifulSoup(html, 'lxml')
		if soup.find('span', class_="next") is None:
			return 0
		else:
			next_url = self.url[:32] + soup.find('span', class_="next").parent['href'][6:-10]
			return next_url


	def getInfo(self, url):
		html = requests.get(url, headers=self.headers).text
		soup = BeautifulSoup(html, 'lxml')
		try:
			articles = soup.find('div', id='content-left').find_all('div', class_='article block untagged mb15')
			for article in articles:
				nickname =  article.find_all('a')[1].text.strip()
				if article.find('div', class_='articleGender manIcon') is not None:
					sex = '男'
					age = article.find('div', class_='articleGender manIcon').get_text()
				elif article.find('div', class_='articleGender womenIcon') is not None:
					sex = '女'
					age = article.find('div', class_='articleGender womenIcon').get_text()
				else:
					sex = '未知'
					age = None
				content = article.find('div', class_='content').get_text()
				if article.find('span', class_='stats-vote').find('i') is not None:
					votes = article.find('span', class_='stats-vote').find('i').get_text()
				else:
					votes = None
				if article.find('span', class_='stats-comments').find('i') is not None:
					comments = article.find('span', class_='stats-comments').find('i').get_text()
				else:
					comments = None

				print nickname, sex, age, votes, comments
				# print content
		except:
			pass

	def getTotal(self):
		url = self.url
		while url:
			print '正在爬取网页：' + url
			self.getInfo(url)
			time.sleep(1)
			url = self.getNextUrl(url)


if __name__ == "__main__":
	qiubai = QiuBai()
	qiubai.getTotal()
