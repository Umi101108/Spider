# -*- coding: utf8 -*-

import requests
import json
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
		url = 'http://music.163.com/#/user/songs/rank?id=371821058'
		url = 'http://music.163.com/weapi/v1/play/record?csrf_token='
		refer = 'http://music.163.com/user/songs/rank?id=371821058'
		# param={'params':'dEaDmN4/oYqVIhuN9BgCa3KEqFuhYu8zNhFLWrAS5R9sWzxoP3uBypNQkthPXVvUPxhDlAfftKcjkVhrEpAOAR7jrphSw6rtHpBtQi658UFRJMr3dZDT5nSIqwtoEpSDQyYTzead16sG44sEsIWHpiXTqRwG/xzWuiMJ6pFV1cRTWKSk5z/o9vanYfuVHeFx','encSecKey':'bdd80b128c4ab823d380f6013d6503f9af156fc47bd48b8bfe970c0b66dd1f9921f6da19d803025a7bb06647144d76f5b803bd88a39a79d576a041a690dc9e70dcba41bd651b7f002a7babf9ed4ab138edbf2022cbaa5f52d05dac0a472b2bcbf6ab930649f6e6edb17a3ae200001dab31a6c8e2203e87576c2b596d51571c03'}#这里每行末尾的‘\’是代码过长用来换行的，慎用，换行多了易出现bug。
		headers = {
			'Referer': refer,
			'User-Agent': self.user_agent,
			'Cookie': 'JSESSIONID-WYYY=IhihdCdm%2F01pIoDVftVVoi4a%5CwI8x9OtmHMoj5lonFu7UTenllimfBgWOnCTiozJi%2BiEifpmYUCJNxqEAneGEneunZP6wh1lNmv6OfhAKP9uG8NsEs9Cdrmdqao7KMSsQIY%2FWlDnx5UjZIkhdE4FgV%2FzAmkJoJ5YMgfIUEXBduzAzuvE%3A1500475598484; _iuqxldmzr_=32; _ntes_nnid=67a88fb8cc9127d324f706770305c34d,1500473798525; _ntes_nuid=67a88fb8cc9127d324f706770305c34d; __utma=94650624.743015140.1500473799.1500473799.1500473799.1; __utmb=94650624.8.10.1500473799; __utmc=94650624; __utmz=94650624.1500473799.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
		}
		params = {
			'params': 'mIp+51R7s1mx9dW0rcoymal+gFM0z+Ici0kPqMNFIklgBuX3RkCLndhvLcZi43hwZMCHF9QvjrrS/ojUUbW9b84IHCzmI/E/HY4TvH5IWkmdTsHMqv3wwvaqfZpEe/f5ZXlOUdWkFDNdaA8gJqK1/juqxp6k6AV1ySY0+2XLmWt0tXkbtzD09CCZKXFLEiU6',
			'encSecKey': 'a4bf46891389db284457d131a4dbd5b6de90c39265a9552c69f3a666c87a84a3c386e9b5ebc81c20b6d8c34b2f39996ffb95d077354354e2a796eb884ae36ddc6a7260c961d1954201d398c7df7c1a23273deb436bbd6c0721fcfee61e507b82f275b162b6c192a4738f19b4ee46860c3007d64e705f92f72e25adb4daf5392d',
		}
		# r=requests.get(url, headers=headers)
		r = requests.post(url, headers=headers, data=params)
		data = json.loads(r.content)
		# for d in data:
		# 	print d
		# print data['weekData']
		all_songs = data.get('allData')
		for songs in all_songs:
			print songs.get('song').get('name')
			print songs.get('song').get('ar')[0].get('name')

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
		# self.getSongs()


if __name__ == "__main__":
	music = Music()
	music.main()
