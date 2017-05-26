# -*- coding: utf-8 -*-

import requests

url = 'http://www.jianshu.com'
url = 'http://www.jianshu.com/?seen_snote_ids%5B%5D=12783954&seen_snote_ids%5B%5D=12187879&seen_snote_ids%5B%5D=12799791&seen_snote_ids%5B%5D=12803717&seen_snote_ids%5B%5D=12748207&seen_snote_ids%5B%5D=12712438&seen_snote_ids%5B%5D=12710784&seen_snote_ids%5B%5D=12735077&seen_snote_ids%5B%5D=12698066&seen_snote_ids%5B%5D=12736519&seen_snote_ids%5B%5D=12755873&seen_snote_ids%5B%5D=12745555&seen_snote_ids%5B%5D=12707395&seen_snote_ids%5B%5D=12740881&seen_snote_ids%5B%5D=12684922&seen_snote_ids%5B%5D=12169263&seen_snote_ids%5B%5D=12589375&seen_snote_ids%5B%5D=12743259&seen_snote_ids%5B%5D=12742335&seen_snote_ids%5B%5D=12710083&seen_snote_ids%5B%5D=12817325&seen_snote_ids%5B%5D=8852442&seen_snote_ids%5B%5D=12809319&seen_snote_ids%5B%5D=12812380&seen_snote_ids%5B%5D=12806950&seen_snote_ids%5B%5D=12815754&seen_snote_ids%5B%5D=12573038&seen_snote_ids%5B%5D=12713215&seen_snote_ids%5B%5D=12817633&seen_snote_ids%5B%5D=12800311&seen_snote_ids%5B%5D=12618840&seen_snote_ids%5B%5D=12799994&seen_snote_ids%5B%5D=12796766&seen_snote_ids%5B%5D=12760010&seen_snote_ids%5B%5D=12750498&seen_snote_ids%5B%5D=12753970&seen_snote_ids%5B%5D=12812596&seen_snote_ids%5B%5D=12806553&seen_snote_ids%5B%5D=12658283&seen_snote_ids%5B%5D=12761472&page=3'


class JianShu(object):

	def __init__(self):
		self.url = 'http://www.jianshu.com'

	def getInfo(self):
		html = requests.get(self.url).content
		print html



if __name__ == '__main__':
	jianshu = JianShu()
	jianshu.getInfo()