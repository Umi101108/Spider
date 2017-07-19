# -*- coding: utf8 -*-

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

class Music(object):

	def __init__(self):
		self.base_url = "http://music.163.com/m/user/home?id=371821058"
		self.songs_url = "http://music.163.com/#/user/songs/rank?id=371821058"
		self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
		self.headers = {'User-Agent': self.user_agent}

	def getSoup(self, url):
		response = requests.get(url, headers=self.headers)
		if response.status_code == 200:
			html = response.content
			soup = BeautifulSoup(html, 'lxml')
			return soup
		else:
			print "该网页不存在"
			return

	def getInfo(self):
		soup = self.getSoup(self.base_url)
		name = soup.select('h2#j-name-wrap > span')[0].get_text()
		level = soup.select('h2#j-name-wrap > span')[1].get_text()
		if soup.select('h2#j-name-wrap > i')[0].get('class')[-1][-1] == '2':
			gender = 'female'
		elif soup.select('h2#j-name-wrap > i')[0].get('class')[-1][-1] == '1':
			gender = 'male'
		else:
			gender = 'unknown'
		event_count = soup.select('ul#tab-box > li > a > strong')[0].get_text()
		follow_count = soup.select('ul#tab-box > li > a > strong')[1].get_text()
		fan_count = soup.select('ul#tab-box > li > a > strong')[2].get_text()
		weibo = soup.select('a[class="u-slg u-slg-sn]"')[0].get('href')
		print name, level, gender, weibo


	def getSongs(self):
		soup = self.getSoup(self.songs_url)
		# print soup.select('div.g-bd')[0].get_text()
		driver = webdriver.Chrome("/Users/umi/Downloads/chromedriver")
		driver.get(self.songs_url)
		print driver.page_source


	def main(self):
		# url='http://music.163.com/weapi/v1/resource/comments/R_SO_4_465920636?csrf_token=c0f6bfdcd0526ec0ba6c207051a08960'
		# url = 'http://music.163.com/#/user/songs/rank?id=371821058'
		# param={'params':'dEaDmN4/oYqVIhuN9BgCa3KEqFuhYu8zNhFLWrAS5R9sWzxoP3uBypNQkthPXVvUPxhDlAfftKcjkVhrEpAOAR7jrphSw6rtHpBtQi658UFRJMr3dZDT5nSIqwtoEpSDQyYTzead16sG44sEsIWHpiXTqRwG/xzWuiMJ6pFV1cRTWKSk5z/o9vanYfuVHeFx','encSecKey':'bdd80b128c4ab823d380f6013d6503f9af156fc47bd48b8bfe970c0b66dd1f9921f6da19d803025a7bb06647144d76f5b803bd88a39a79d576a041a690dc9e70dcba41bd651b7f002a7babf9ed4ab138edbf2022cbaa5f52d05dac0a472b2bcbf6ab930649f6e6edb17a3ae200001dab31a6c8e2203e87576c2b596d51571c03'}#这里每行末尾的‘\’是代码过长用来换行的，慎用，换行多了易出现bug。

		# r=requests.post(url, param)

		# data=r.text#data得到的就是json
		# print data
		# self.getInfo()
		# driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
		# driver = webdriver.Chrome("/Users/umi/Downloads/chromedriver")
		# driver.get(self.base_url)
		# time.sleep(5)
		# elem_songsall = driver.find_element_by_xpath('//*[@id="songsall"]')
		# elem_songsall.click()
		# time.sleep(5)
		# elem_songsmore = driver.find_element_by_xpath('//div[@class="more"]/a')
		# elem_songsmore.click()
		self.getSongs()


if __name__ == "__main__":
	music = Music()
	music.main()
