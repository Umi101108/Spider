# -*- coding: utf-8 -*-

import requests
import time
import random
import json
import MySQLdb
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.webdriver.support.ui as ui


class YaoZhi(object):

	def __init__(self):
		self.user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
		self.cookies = ""
		self.cookies = "UtzD_f52b_saltkey=AAE2a2iE; UtzD_f52b_lastvisit=1503983261; yaozh_mobile=1; yaozh_uidhas=1; ad_download=1; UtzD_f52b_ulastactivity=1498699308%7C0; yaozh_mylogin=1504161343; PHPSESSID=u91kn0ttes4lr5r07luuk467u3; expire=1504573461225; _ga=GA1.2.1733785226.1503986776; _gid=GA1.2.360414851.1504487155; yaozh_logintime=1504487145; yaozh_user=418369%09%E4%B8%8A%E6%B5%B7%E5%81%A5%E6%99%B4%E4%BF%A1%E6%81%AF; yaozh_userId=418369; db_w_auth=400818%09%E4%B8%8A%E6%B5%B7%E5%81%A5%E6%99%B4%E4%BF%A1%E6%81%AF; UtzD_f52b_creditnotice=0D0D2D0D0D0D0D0D0D400818; UtzD_f52b_creditbase=0D0D10D0D0D0D0D0D0; UtzD_f52b_creditrule=%E6%AF%8F%E5%A4%A9%E7%99%BB%E5%BD%95; UtzD_f52b_lastact=1504487146%09uc.php%09; UtzD_f52b_auth=5a07iRtHwIuLqYC4SGHDZMB3qGKwwRDEWGypygrxmog%2Bv35I3B0K6aqTQdaGsrA7py%2FSbdpf%2FUa7SVPc9hJVIIiBixY; think_language=zh-CN; zbpreid=; WAF_SESSION_ID=08d30abe81bf1c35b31c9362b052e2e7; _ga=GA1.3.1733785226.1503986776; Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94=1504055893,1504140650,1504228185,1504487058; Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94=1504511570"
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
		self.yaopinzhongbiao_url = "https://db.yaozh.com/yaopinzhongbiao?first={province}&p={p}&pageSize=30&zb_approvaldateend={end}&zb_approvaldatestr={str}"


	def getSoup(self, url, retry=1):
		response = requests.get(url, headers=self.headers, stream=True, timeout=15)
		if response.status_code == 200:
			html = response.content
			soup = BeautifulSoup(html, 'lxml')
			# if soup.select('body[onload="challenge();"]'):
			# 	print 2333
			# 	print response.url
			# 	time.sleep(random.randint(60, 70))
			# 	self.getSoup(response.url)
			# elif soup.select('.responsive-table'):
			# 	return soup
			# soup
			print soup
			# print soup.select('table.table-striped')
			if soup.select('table.table-striped'):
				print 666
				return soup
			elif soup.select('div[data-widget="dbNoData"]'):
				print "No Data"
				return None
			elif soup.select('body[onload="challenge();"]') or retry < 10:
				print 233333
				time.sleep(70)
				retry += 1
				self.getSoup(url, retry)
			else:
				print "无能为力"
		else:
			print "该网页不存在"
			return '???'

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
		startyear = 2017
		endyear = 2017
		startmonth = 8
		endmonth = 12
		startday = 1
		endday = 28
		yearsecends = []
		for y in xrange(startyear, endyear+1):
			for m in xrange(startmonth, endmonth+1):
				for d in xrange(startday, endday+1, 2):
					date ='%d-%02d-%02d' % (y, m, d)
					secend.append(date)
		for s in xrange(len(secend)-1):
			yearsecends.append((secend[s],secend[s+1]))
		return yearsecends

	def getInteraction(self, p=150, pagesize=30):
		table = "interaction2"
		for i in xrange(p):
			print i
			# try:
			url = self.interaction_url.format(i, pagesize)
			soup = self.getSoup(url)
			# print soup
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
				# self.insertData(table, content)
			time.sleep(random.randint(2, 8))
			# except:
			# 	time.sleep(10)
			# if i%13 == 0:
			# 	time.sleep(1)
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
					time.sleep(random.randint(5, 13))
				time.sleep(random.randint(12, 25))
			except:
				pass


	def getYaopinzhongbiao(self):
		table = "yaopinzhongbiao"
		url = self.yaopinzhongbiao_url
		soup = self.getSoup(url)
		info_list = soup.select('tbody tr')
		for info in info_list:
			id = info.select('input')[0]['value']
			yptym = info.select('td')[1].get_text()
			spm = info.select('td')[2].get_text()
			jx = info.select('td')[3].get_text()
			gg = info.select('td')[4].get_text()
			bzzhb = info.select('td')[5].get_text()
			dw = info.select('td')[6].get_text()
			zbj = info.select('td')[7].get_text()
			zlcc = info.select('td')[8].get_text()
			scqy = info.select('td')[9].get_text()
			tbqy = info.select('td')[10].get_text()
			zbsf = info.select('td')[11].get_text()
			fbrq = info.select('td')[12].get_text()
			bz = info.select('td')[13].get_text()
			lywj = info.select('td')[14].get_text()
			lywj_url = info.select('td')[14].a.get('href', '') if info.select('td')[14].a else ''
			print lywj_url
			zscp = info.select('td')[15].get_text()
			print id, yptym, spm, jx, gg, bzzhb, dw, zbj, zlcc, scqy, tbqy, zbsf, fbrq, bz, lywj, lywj_url
			content = {
				"id": id,
				"yptym": yptym, 
				"spm": spm, 
				"jx": jx,
				"gg": gg,
				"bzzhb": bzzhb, 
				"dw": dw,
				"zbj": zbj,
				"zlcc": zlcc,
				"scqy": scqy,
				"tbqy": tbqy,
				"zbsf": zbsf,
				"fbrq": fbrq,
				"bz": bz,
				"lywj": lywj,
				"lywj_url": lywj_url,
				"zscp": zscp
			}

	def getYibao(self):
		print 'yibao'
		ybdq = soup.select()
		bh = soup.select()
		ypmc = soup.select()
		ywmc = soup.select()
		jx = soup.select()
		yplb = soup.select()
		yblx = soup.select()

	def getPageSource(self):
		driver = webdriver.PhantomJS(r"E:\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe")
		# driver = webdriver.Chrome("D:\chromedriver_win32\chromedriver.exe")
		driver.get(self.yaopinzhongbiao_url)
		wait = ui.WebDriverWait(driver, 15)
		wait.until(lambda driver: driver.find_element_by_xpath('//table[@class="table table-striped"]'))
		print driver.page_source
		print 2333
		driver.quit()


	def main(self):
		for startdate, enddate in self.getYearsecend():
			print startdate, enddate
			for province in self.provinces:
				url = self.yaopinzhongbiao_url.format(province=province, p=1, str=startdate, end=enddate)
				print url
				try:
					max_page = self.getMaxpage(url)
					print max_page
				except:
					pass
							


if __name__ == "__main__":
	yaozhi = YaoZhi()
	# yaozhi.getInteraction()
	url = yaozhi.interaction_url.format(2, 30)
	# url = yaozhi.yaopinzhongbiao_url
	# print url
	# print yaozhi.getSoup(url)
	# print yaozhi.getSoup(url).select('body[onload="challenge();"]')
	# yaozhi.getYaopinjiage()
	# print yaozhi.getYearsecend()
	# print yaozhi.getMaxpage(url)
	# yaozhi.getYaopinzhongbiao()
	# yaozhi.getPageSource()
	yaozhi.main()
