# -*- coding: utf-8 -*-

import requests
import json

class WeiBo(object):

	def __init__(self):
		self.url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={0}&containerid=107603{0}&page={1}'

	def getInfo(self, url):
		response = requests.get(url)
		ob_json = json.loads(response.text)
		print ob_json['mblog']['id']


if __name__ == "__main__":
	weibo = WeiBo()
	weibo.getInfo(weibo.url.format('1713926427','1'))

