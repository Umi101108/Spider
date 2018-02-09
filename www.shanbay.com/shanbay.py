# -*- coding: utf-8 -*-
import re
import math
import requests
from bs4 import BeautifulSoup

class Shanbay(object):

	def __init__(self):
		self.user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
		self.headers = {'User-Agent': self.user_agent}
		self.result = []

	def getUnits(self, book_url):
		response = requests.get(book_url)
		html = response.content
		soup = BeautifulSoup(html, 'lxml')
		units = soup.select('td.wordbook-wordlist-name > a[href]')
		units = ['https://www.shanbay.com'+unit.get('href') for unit in units]
		return units

	def getList(self, url):
		response = requests.get(url)
		html = response.content
		soup = BeautifulSoup(html, 'lxml')
		word_list = soup.select('table.table > tbody > tr')
		for word in word_list:
			self.result.append((word.select('strong')[0].get_text(), word.select('td.span10')[0].get_text().replace("\n", " ")))

	def getAllList(self, unit_url):
		response = requests.get(unit_url)
		html = response.content
		soup = BeautifulSoup(html, 'lxml')
		pagenum = math.ceil(float(soup.select('div.span6 h4 span')[0].get_text())/20)
		for page in xrange(1, int(pagenum)+1):
			url = unit_url + '?page=' + str(page)
			self.getList(url)

	def writeMd(self, filename):
		with open(filename, 'w') as f:
			f.write("| word | paraphrase | \n | ---- | ---- | \n")
			for r in self.result:
				f.write("| {word} | {paraphrase} |\n".format(word=r[0], paraphrase=r[1]))
			

	def main(self):
		book_url = 'https://www.shanbay.com/wordbook/167197/'
		units = self.getUnits(book_url)
		for unit in units:
			self.getAllList(unit)
		for r in self.result:
			print r[0], r[1]

		filename = 'python_word.md'
		self.writeMd(filename)


if __name__ == "__main__":
	Shanbay().main()
		

