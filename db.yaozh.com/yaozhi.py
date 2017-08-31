# -*- coding: utf-8 -*-

import requests
import time
import random
import json
import MySQLdb
from bs4 import BeautifulSoup

class YaoZhi(object):

	def __init__(self):
		self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
		self.cookies = ""
		self.cookies = "UtzD_f52b_saltkey=AAE2a2iE; UtzD_f52b_lastvisit=1503983261; yaozh_mobile=1; yaozh_uidhas=1; ad_download=1; UtzD_f52b_ulastactivity=1498699308%7C0; PHPSESSID=jj0a2kl6ub78ft17ndn5pkil45; expire=1504227053337; UtzD_f52b_creditnotice=0D0D2D0D0D0D0D0D0D400818; UtzD_f52b_creditbase=0D0D6D0D0D0D0D0D0; UtzD_f52b_creditrule=%E6%AF%8F%E5%A4%A9%E7%99%BB%E5%BD%95; yaozh_logintime=1504158655; yaozh_user=418369%09%E4%B8%8A%E6%B5%B7%E5%81%A5%E6%99%B4%E4%BF%A1%E6%81%AF; yaozh_userId=418369; db_w_auth=400818%09%E4%B8%8A%E6%B5%B7%E5%81%A5%E6%99%B4%E4%BF%A1%E6%81%AF; UtzD_f52b_lastact=1504158665%09uc.php%09; UtzD_f52b_auth=bb18B%2FjxxhpZZ1wfB8fSXMjE0q1FsCV%2B1cuoLnURgWHrV33KhRwb78IHkW7MvzmNTPEQdRtqMUeIKXcWGTQzSmeeZ0Y; yaozh_mylogin=1504161343; _ga=GA1.2.1733785226.1503986776; _gid=GA1.2.175072032.1504080499; WAF_SESSION_ID=1ca244fb8ec96dc324a8ceacf4f0a8c1; think_language=zh-CN; _ga=GA1.3.1733785226.1503986776; _gat=1; Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94=1503986776,1504003025,1504055893,1504140650; Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94=1504167774"
		self.headers = {'User-Agent': self.user_agent, 'Cookie': self.cookies}
		try:
			self.conn = MySQLdb.connect(
					host = 'localhost',
					port = 3306,
					user = 'root', 
					passwd = 'gt123456',
					db = 'yaozhi'
				)
			self.cur = self.conn.cursor()
		except MySQLdb.Error, e:
			print "数据库连接错误，原因为%d: %s" % (e.args[0], e.args[1])
		self.provinces = ["北京", "福建", "河南", "江苏", "江西", "上海", "天津", "浙江", "海南", "湖北", "湖南", "山东", "重庆", "广东", "贵州", "河北", "吉林", "辽宁", "宁夏", "山西", "安徽", "甘肃", "广西", "内蒙古", "青海", "陕西", "四川", "西藏", "新疆", "云南", "黑龙江", "国家"]
		self.interaction_url = "https://db.yaozh.com/interaction?p={}&pageSize={}"
		self.yaopinjiage_url = "https://db.yaozh.com/yaopinjiage?firstjiage={}&p={}&pageSize=30&yearsecendend={}&yearsecendstr={}"


	def getSoup(self, url):
		response = requests.get(url, headers=self.headers, timeout=10)
		if response.status_code == 200:
			html = response.content
			soup = BeautifulSoup(html, 'lxml')
			if soup.select('body[onload="challenge();"]'):
				print 2333
				time.sleep(random.randint(2, 10))
				self.getSoup(response.url)
			return soup
		else:
			print "该网页不存在"
			return 

	def insertData(self, table, my_dict):
		try:
			self.conn.set_character_set('utf8')
			cols = ', '.join(my_dict.keys())
			values = '", "'.join(my_dict.values())
			sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, '"' + values + '"')
			try:
				result = self.cur.execute(sql)
				insert_id = self.conn.insert_id()
				self.conn.commit()
				if result:
					return insert_id
				else:
					return 0
			except MySQLdb.Error, e:
				self.conn.rollback()
				if "key 'PRIMARY'" in e.args[1]:
					print "数据已存在，未插入数据"
				else:
					print "数据插入失败，原因 %d: %s" % (e.args[0], e.args[1])
		except MySQLdb.Error, e:
			print "数据库错误，原因 %d: %s" % (e.args[0], e.args[1])

	def getProvince(self):
		url = self.yaopinjiage_url
		soup = self.getSoup(url)
		provinces = soup.select('select.form-control')[0].get('data-list')[2:-2].split('},{')
		for p in provinces:
			p_name = eval('{'+p+'}')['name'].decode('raw_unicode_escape')
			pr.append(p_name.encode('utf8'))
		print json.dumps(pr[1:],ensure_ascii=False)

	def getMaxpage(self, url):
		soup = self.getSoup(url)
		data_size = 30
		# max_page = soup.select('.tr.offset-top')[0].get('data-max-page')
		data_total = soup.select('.tr.offset-top')[0].get('data-total')
		max_page = int(data_total)/data_size + 1
		return max_page

	def getYearsecend(self):
		secend = []
		startyear = 2000
		endyear = 2017
		startmonth = 1
		endmonth = 12
		startday = 1
		yearsecends = []
		for y in xrange(startyear, endyear+1):
			for m in xrange(startmonth, endmonth+1):
				date ='%d-%02d-01' % (y, m)
				secend.append(date)
		for s in xrange(len(secend)-1):
			yearsecends.append((secend[s],secend[s+1]))
		return yearsecends

	def getInteraction(self, p=150, pagesize=30):
		table = "interaction2"
		for i in xrange(p):
			print i
			try:
				url = self.interaction_url.format(i, pagesize)
				soup = self.getSoup(url)
				info_list = soup.select('tbody tr')
				for info in info_list:
					# print info
					ypmc = info.select('th')[0].get_text()
					xhzydyp = info.select('td')[0].get_text()
					zyxg = info.select('td')[1].get_text()
					print ypmc, xhzydyp
					content = {
						"ypmc": ypmc,
						"xhzydyp": xhzydyp,
						"zyxg": zyxg
					}
					self.insertData(table, content)
				time.sleep(random.randint(2, 8))
			except:
				time.sleep(10)
			if i%10 == 0:
				time.sleep(60)
		return 

	def getYaopinjiage(self, jiage=32, p=3):
		table = "yaopinjiage"
		pr = []
		for startdate, enddate in self.getYearsecend():
			print startdate, enddate
			# for i in xrange(1, jiage):
			# 	print i
			i = '全部'
			url = self.yaopinjiage_url.format(i, 1, enddate, startdate)
			try:
				p = self.getMaxpage(self.yaopinjiage_url.format(i, 1, enddate, startdate))
				for j in xrange(p):
					try:
						url = self.yaopinjiage_url.format(i, j, enddate, startdate)
						soup = self.getSoup(url)
						info_list = soup.select('tbody tr')
						for info in info_list:
							# print info
							djdq = info.select('th')[0].get_text()
							ypmc = info.select('a.cl-blue')[0].get_text()
							ypmc_url = info.select('a.cl-blue')[0]['href']
							jx = info.select('td')[1].get_text()
							gg = info.select('td')[2].get_text()
							dw = info.select('td')[3].get_text()
							zglsj = info.select('td')[4].get_text()
							scqy = info.select('td')[5].get_text()
							bz = info.select('td')[6].get_text()
							zxrq = info.select('td')[7].get_text()
							wjh = info.select('td')[8].get_text()
							print djdq, ypmc, jx, gg, dw, zglsj, scqy, bz, zxrq, wjh
							content = {
								"djdq": djdq,
								"ypmc": ypmc,
								"ypmc_url": ypmc_url,
								"jx": jx,
								"gg": gg,
								"dw": dw,
								"zglsj": zglsj,
								"scqy": scqy,
								"bz": bz,
								"zxrq": zxrq,
								"wjh": wjh
							}
							self.insertData(table, content)
					except:
						time.sleep(20)
						pass
				time.sleep(random.randint(2, 5))
			except:
				pass

	def getYibao(self):
		print 'yibao'
		ybdq = soup.select()
		bh = soup.select()
		ypmc = soup.select()
		ywmc = soup.select()
		jx = soup.select()
		yplb = soup.select()
		yblx = soup.select()
						


if __name__ == "__main__":
	yaozhi = YaoZhi()
	yaozhi.getInteraction()
	# url = yaozhi.interaction_url.format(2, 30)
	# print url
	# print yaozhi.getSoup(url)
	# print yaozhi.getSoup(url).select('body[onload="challenge();"]')
	# yaozhi.getYaopinjiage()
	# print yaozhi.getMaxpage(url)
