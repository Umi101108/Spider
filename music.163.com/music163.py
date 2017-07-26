# -*- coding: utf8 -*-

import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time

class Music(object):

	def __init__(self):
		self.base_url = "http://music.163.com/user/home?id=371821058"
		self.rank_url = "http://music.163.com/user/songs/rank?id=371821058"
		self.playlist_url = "http://music.163.com/playlist?id=525591083"
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

	def getUserInfo(self):
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
		try:
			weibo = soup.select('a[class="u-slg u-slg-sn"]')[0].get('href')
		except:
			weibo = None
		print name, level, gender, weibo

	def getFavPlaylist(self):
		# driver = webdriver.Chrome("/Users/umi/Downloads/chromedriver")
		driver = webdriver.PhantomJS("/Users/umi/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs")
		driver.get(self.base_url)
		driver.switch_to_frame('g_iframe')
		try:
			wait = ui.WebDriverWait(driver, 15)
			wait.until(lambda driver: driver.find_element_by_xpath('//*[@class="m-cvrlst f-cb"]/li[1]/div/a'))
			urls = driver.find_elements_by_xpath('//*[@class="m-cvrlst f-cb"]/li[1]/div/a')
			# print urls.text
			favourite_url = urls[0].get_attribute("href")
			print favourite_url
			print urls[1].get_attribute("href")
			# print driver.page_source
		except Exception as e:
			print e
		# finally:
		# 	driver.quit()

	def getFavSongs(self):
		driver = webdriver.PhantomJS("/Users/umi/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs")
		driver.get(self.playlist_url)
		driver.switch_to_frame('g_iframe')
		m_table = driver.find_elements_by_xpath('//*[@class="j-flag"]/table/tbody/tr')
		for m in m_table:
			# print '|'.join(m.text.split('\n'))
			no = m.find_element_by_xpath('./td[@class="left"]').text
			song_id = m.find_element_by_xpath('.//div[@class="f-cb"]//a').get_attribute("href")
			song_title = m.find_element_by_xpath('.//div[@class="f-cb"]//b').text
			artist = m.find_element_by_xpath('.//div[@class="text"]/span').text
			album_name = m.find_element_by_xpath('.//div[@class="text"]/a[last()]').text
			print song_id
			print no, song_title, artist, album_name

	def getRank2(self):
		# driver = webdriver.Chrome("/Users/umi/Downloads/chromedriver")
		driver = webdriver.PhantomJS("/Users/umi/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs")
		driver.get(self.rank_url)
		driver.switch_to_frame('g_iframe')
		wait = ui.WebDriverWait(driver, 15)
		wait.until(lambda driver: driver.find_element_by_xpath('//div[@id="m-record"]/div/div/ul'))
		span_songsall = driver.find_element_by_id('songsall')
		span_songsall.click()
		time.sleep(5)
		songsall = driver.find_elements_by_xpath('//div[@id="m-record"]/div/div/ul/li')
		for song in songsall:
			print song.text
			print song.get_attribute('id')
		# print driver.page_source

	def getRank(self):
		url = 'http://music.163.com/weapi/v1/play/record?csrf_token='
		refer = 'http://music.163.com/user/songs/rank?id=371821054'
		headers = {
			'Referer': refer,
			'User-Agent': self.user_agent,
		}
		params = {
			'params': 'mIp+51R7s1mx9dW0rcoymal+gFM0z+Ici0kPqMNFIklgBuX3RkCLndhvLcZi43hwZMCHF9QvjrrS/ojUUbW9b84IHCzmI/E/HY4TvH5IWkmdTsHMqv3wwvaqfZpEe/f5ZXlOUdWkFDNdaA8gJqK1/juqxp6k6AV1ySY0+2XLmWt0tXkbtzD09CCZKXFLEiU6',
			'encSecKey': 'a4bf46891389db284457d131a4dbd5b6de90c39265a9552c69f3a666c87a84a3c386e9b5ebc81c20b6d8c34b2f39996ffb95d077354354e2a796eb884ae36ddc6a7260c961d1954201d398c7df7c1a23273deb436bbd6c0721fcfee61e507b82f275b162b6c192a4738f19b4ee46860c3007d64e705f92f72e25adb4daf5392d',
		}
		r = requests.post(url, headers=headers, data=params)
		data = json.loads(r.content)
		all_songs = data.get('allData')
		for songs in all_songs:
			song_score = songs.get('score')
			song_id = songs.get('song').get('id')
			song_name = songs.get('song').get('name')
			artist_id = songs.get('song').get('ar')[0].get('id')
			artist_name = songs.get('song').get('ar')[0].get('name')
			album_id = songs.get('song').get('al').get('id')
			album_name = songs.get('song').get('al').get('name')
			print song_id, song_name, artist_id, artist_name, album_id, album_name, song_score

	def main(self):
		# self.getFavPlaylist()
		# self.getFavSongs()
		self.getRank2()

if __name__ == "__main__":
	music = Music()
	music.main()
