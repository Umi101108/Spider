# -*- coding: utf-8 -*-

import datetime
import requests
from bs4 import BeautifulSoup


class Github(object):

	def __init__(self):
		self.base_url = 'https://github.com/trending/{language}'
		self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
		self.headers = {'User-Agent': self.user_agent}

	def getInfo(self, url):
		html = requests.get(url, headers=self.headers).text
		soup = BeautifulSoup(html, 'lxml')
		lists = soup.find('div', class_="explore-content").find_all('li', class_="col-12 d-block width-full py-4 border-bottom")
		for l in lists:
			title = l.find('div', class_="d-inline-block col-9 mb-1").get_text().strip()
			url = 'https://github.com' + l.find('div', class_="d-inline-block col-9 mb-1").a['href']
			star = l.find('a', class_="muted-link mr-3").get_text().strip().replace(',', '')
			content = l.find('div', class_="py-1").get_text().strip()
			print title, url, star, '\n'+content

	def getTotal(self, language):
		url = self.base_url.format(language=language)
		self.getInfo(url)

	def main(self):
		languages = ['c++', 'css', 'html', 'javascript', 'objective-c', 'python']
		for lg in languages:
			self.getTotal(lg)


if __name__ == "__main__":
	github = Github()
	github.main()