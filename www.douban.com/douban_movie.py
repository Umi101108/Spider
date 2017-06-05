# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time


class DouBan(object):

	def __init__(self):
		self.base_url = 'https://movie.douban.com/top250'
		self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
		self.headers = {'User-Agent': self.user_agent}
		self.result = []

	def getInfo(self, url):
		html = requests.get(url).content
		soup = BeautifulSoup(html, 'lxml')
		movies = soup.find('ol', class_="grid_view").find_all('li')
		for movie in movies:
			name = movie.find('div', class_="pic").a.img['alt']
			star = movie.find('div', class_="star").find('span', class_="rating_num").get_text()
			people_num = movie.find('div', class_="star").find_all('span')[-1].get_text()
			try:
				quote = movie.find('p', class_="quote").get_text()
			except:
				quote = None
			url = movie.find('a')['href']
			# print name, star, people_num, quote, url
			movie = {
				"name": name,
				"star": star,
				"people_num": people_num,
				"quote": quote,
				"url": url
			}
			self.result.append(movie)
		next_url = soup.find('span', class_="next").a
		if next_url is not None:
			time.sleep(1)
			self.getInfo(self.base_url + next_url['href'])
		else:
			return None

	def getTotal(self):
		url = self.base_url
		self.getInfo(url)
		for r in self.result:
			print r


	def getDetail(self, url):
		html = requests.get(url).content
		soup = BeautifulSoup(html, 'lxml')
		indent = soup.find('div', class_="related-info").find('div', class_="indent").get_text().strip()
		print indent


if __name__ == "__main__":
	douban = DouBan()
	douban.getTotal()