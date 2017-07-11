# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import time


class Smzdm(object):

	def __init__(self):
		# self.base_url = "http://www.smzdm.com/p/1000211/"
		# self.base_url = "http://www.smzdm.com/p/7502199/"
		self.base_url = "http://www.smzdm.com/p/7516118/"
		self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
		self.headers = {'User-Agent': self.user_agent}

	def getInfo(self, url):

		soup = self.getSoup(url)

		article_title = soup.select('.article_title > em[itemprop="name"]')[0].get_text().lstrip()
		price = soup.select('.article_title > em > span')[0].get_text().strip()

		fav_num = soup.select('div.leftLayer > a.fav')[0].get_text()
		comment_num = soup.select('div.leftLayer > a.comment')[0].get_text()

		self.getTag(soup)
		self.getRating(soup)

		if soup.select('.comment_wrap'):
			try:
				pageno = soup.select('.comment_wrap > div.tab_info > ul.pagination > li')[-4].get_text()
			except:
				pageno = 1

			for p in xrange(1, int(pageno)+1):
				url2 = self.base_url + 'p{}/'.format(str(p))
				soup2 = self.getSoup(url2)
				self.getComment(soup2)
		else:
			print "暂无评论"


	def getSoup(self, url):
		response = requests.get(url, headers=self.headers)
		if response.status_code == 200:
			html = response.content
			soup = BeautifulSoup(html, 'lxml')
			return soup
		else:
			print "该网页不存在"
			return


	def getRating(self, soup):
		rating_all_num = soup.select('#rating_all_num > em')[0].get_text()
		rating_worthy_num = soup.select('#rating_worthy_num')[0].get_text().strip()
		rating_unworthy_num = soup.select('#rating_unworthy_num')[0].get_text().strip()


	def getTag(self, soup):
		tags = soup.select('.meta-tags')
		tag_meta = {}
		for tag in tags:
			tag_sort = tag.select('div')[0].get_text().split(u'：')[0] if tag.select('div') else '暂无分类'
			tag_detail = tag.select('a')[0].get_text()
			tag_meta[tag_detail] = tag_sort


	def getComment(self, soup):
		comment_listBox = soup.select("div#commentTabBlockNew > ul.comment_listBox")[0]
		comments = comment_listBox.select('li.comment_list')
		for comment in comments:
			grey = comment.select('span')[0].get_text()
			usmzdmid = comment.select('a.a_underline')[0].get('usmzdmid')
			author = comment.select('span[itemprop="author"]')[0].get_text()
			rank = comment.select('div.rank')[0].get('title') if comment.select('div.rank') else '0'
			comment_con = comment.select('div.comment_conWrap')[-1].select('div.comment_con > p')[0].get_text()
			dingnum = comment.select('div.comment_action > a.dingNum > span')[0].get_text()
			cainum = comment.select('div.comment_action > a.caiNum > span')[0].get_text()
			print usmzdmid, author, re.sub('\D', '', rank), comment_con, re.sub('\D', '', dingnum)

	def main(self):
		self.getInfo(self.base_url)


if __name__ == '__main__':
	smzdm = Smzdm()
	smzdm.main()
