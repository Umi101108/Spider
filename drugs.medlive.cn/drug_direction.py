# -*- coding: utf-8 -*-

import requests
import time
import csv
import re
from bs4 import BeautifulSoup
import MySQLdb

class DrugDirection(object):

	def __init__(self):
		self.base_url = 'http://drugs.medlive.cn/drugref/html/{pageno}.shtml'
		self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
		self.headers = {'User-Agent': self.user_agent}
		self.writer = csv.writer(file('directions.csv', 'w'))
		try:
			self.conn = MySQLdb.connect(
				host = 'localhost',
				port = 3306,
				user = 'root',
				passwd = 'gt123456',
				db = 'directions'
				)
			self.cur = self.conn.cursor()
		except MySQLdb.Error, e:
			print "连接数据库错误，原因%d: %s" % (e.args[0], e.args[1])


	def download(self, pageno):
		url = self.base_url.format(pageno=str(pageno))
		response = requests.get(url, headers=self.headers)
		response.encoding = 'utf-8'

		if response.status_code == 200:
			text = response.text
			soup = BeautifulSoup(response.text, 'lxml')
			info_left = soup.find('div', class_="info-left")
			self.writer.writerow([pageno, info_left])
		else:
			print response.status_code
			print 'error'

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
				if "key ‘PRIMARY'" in e.args[1]:
					print "数据已存在，未插入数据"
				else:
					print "数据插入失败，原因 %d: %s" % (e.args[0], e.args[1])
		except MySQLdb.Error, e:
			print "数据库错误，原因 %d: %s" % (e.args[0], e.args[1])


	def moreInformation(self, name):
		if name is not None:
			# print "has " + name['name']
			more_information = name.parent.parent.find('div', class_="more-infomation").text.strip()
			return more_information
		else:
			return None

	def structure(self, line):
		text = line[1]
		# Soup = BeautifulSoup(text, 'lxml')
		Soup = BeautifulSoup(text, 'html.parser')
		# 药品名称
		genericNameFormat = Soup.find(attrs={"name": "genericNameFormat"})
		# 药品名称2
		genericName = Soup.find(attrs={"name": "genericName"})
		# 警示语
		warningsMarks = Soup.find(attrs={"name": "warningsMarks"})
		# 成分
		ingredients = Soup.find(attrs={"name": "ingredients"})
		# 性状
		characters = Soup.find(attrs={"name": "characters"})
		# 放射性活度和标识时间
		radioactivityAndTime = Soup.find(attrs={"name": "radioactivityAndTime"})
		# 作用类别
		cationCategory = Soup.find(attrs={"name": "cationCategory"})
		# 适应症
		indications = Soup.find(attrs={"name": "indications"})
		# 功能主治
		effectsAndIndications = Soup.find(attrs={"name": "effectsAndIndications"})
		# 规格
		specification = Soup.find(attrs={"name": "specification"})
		# 用法用量
		dosageAndAdministration = Soup.find(attrs={"name": "dosageAndAdministration"})
		# 不良反应
		adverseReactions = Soup.find(attrs={"name": "adverseReactions"})
		# 禁忌
		contraindications = Soup.find(attrs={"name": "contraindications"})
		# 警告
		warning = Soup.find(attrs={"name": "warning"})
		# 注意事项
		cautions = Soup.find(attrs={"name": "cautions"})
		# 孕妇及哺乳期妇女用药
		pregnancyAndNursingMothers = Soup.find(attrs={"name": "pregnancyAndNursingMothers"})
		# 儿童用药
		pediatricUse = Soup.find(attrs={"name": "pediatricUse"})
		# 老年用药
		geriatricUse = Soup.find(attrs={"name": "geriatricUse"})
		# 药物相互作用
		list_interaction = Soup.find(attrs={"name": "list_interaction"})
		# 药物过量
		overdosage = Soup.find(attrs={"name": "overdosage"})
		# 临床试验
		clinicalTrails = Soup.find(attrs={"name": "clinicalTrails"})
		# 药理毒理
		pharmacologicalAndToxicological = Soup.find(attrs={"name": "pharmacologicalAndToxicological"})
		# 药代动力学
		pharmacokinetics = Soup.find(attrs={"name": "pharmacokinetics"})
		# 贮藏
		storage = Soup.find(attrs={"name": "storage"})
		# 包装
		package = Soup.find(attrs={"name": "package"})
		# 有效期
		usefulLife = Soup.find(attrs={"name": "usefulLife"})
		# 执行标准
		implementStandard = Soup.find(attrs={"name": "implementStandard"})
		# 批准文号
		approvalNo = Soup.find(attrs={"name": "approvalNo"})
		# 进口药品注册证号
		registerNo = Soup.find(attrs={"name": "registerNo"})
		# 进口许可证号
		importLicenceNo = Soup.find(attrs={"name": "importLicenceNo"})
		# 生产企业
		corporationID = Soup.find(attrs={"name": "corporationID"})
		# 妊娠分级
		add1 = Soup.find(attrs={"name": "add1"})
		# 哺乳期分级
		nursing_grading = Soup.find(attrs={"name": "nursing_grading"})

		commonname = ''
		tradename = ''
		englishname = ''
		pinyin = ''
		if genericNameFormat is None:
			genericNameFormat = genericName
		if genericNameFormat is not None:
			commonname = ''
			tradename = ''
			englishname = ''
			pinyin = ''
			more_information = genericNameFormat.parent.parent.find('div', class_="more-infomation")
			str_information = unicode(more_information)

			pattern = re.compile(ur'【通用名称】</label>(.*?)<', re.S)
			tymc = re.search(pattern, str_information)
			if tymc:
				commonname = tymc.group(1).replace('\t','').strip()

			pattern = re.compile(ur'【商品名称】 </label>(.*?)<', re.S)
			spmc = pattern.search(str_information)
			if spmc:
				tradename =  spmc.group(1).replace('\t', '').replace('\r\n', ' ').strip()

			pattern = re.compile(ur'【英文名称】 </label>(.*?)<', re.S)
			ywmc = pattern.search(str_information)
			if ywmc:
				englishname = ywmc.group(1).replace('\t','').strip()

			pattern = re.compile(ur'汉语拼音】 </label>(.*?)<', re.S)
			hypy = pattern.search(str_information)
			if hypy:
				pinyin = hypy.group(1).replace('\t','').strip()

		corporation = ''
		if corporationID is not None:
			more_information = corporationID.parent.parent.find('div', class_="more-infomation")
			str_information = unicode(more_information)
			pattern = re.compile('class="guige">(.*?)<', re.S)
			scqy = pattern.search(str_information)
			if scqy:
				# print "has corporation"
				corporation =  scqy.group(1).strip()

		content = {
			"commonname": commonname,
			"tradename": tradename,
			"englishname": englishname,
			"pinyin": pinyin,
			"warningsMarks": self.moreInformation(warningsMarks),
			"ingredients": self.moreInformation(ingredients),
			"characters": self.moreInformation(characters),
			"radioactivityAndTime": self.moreInformation(radioactivityAndTime),
			"cationCategory": self.moreInformation(cationCategory),
			"indications": self.moreInformation(indications),
			"effectsAndIndications": self.moreInformation(effectsAndIndications),
			"specification": self.moreInformation(specification),
			"dosageAndAdministration": self.moreInformation(dosageAndAdministration),
			"adverseReactions":	self.moreInformation(adverseReactions),
			"contraindications": self.moreInformation(contraindications),
			"warning": self.moreInformation(warning),
			"cautions": self.moreInformation(cautions),
			"pregnancyAndNursingMothers": self.moreInformation(pregnancyAndNursingMothers),
			"pediatricUse": self.moreInformation(pediatricUse),
			"geriatricUse": self.moreInformation(geriatricUse),
			"list_interaction": self.moreInformation(list_interaction),
			"overdosage": self.moreInformation(overdosage),
			"clinicalTrails": self.moreInformation(clinicalTrails),
			"pharmacologicalAndToxicological": self.moreInformation(pharmacologicalAndToxicological),
			"pharmacokinetics": self.moreInformation(pharmacokinetics),
			"storage": self.moreInformation(storage),
			"package": self.moreInformation(package),
			"usefulLife": self.moreInformation(usefulLife),
			"implementStandard": self.moreInformation(implementStandard),
			"approvalNo": self.moreInformation(approvalNo),
			"registerNo": self.moreInformation(registerNo),
			"importLicenceNo": self.moreInformation(importLicenceNo),
			"corporationname": corporation
			# "add1": self.moreInformation(add1),
			# "nursing_grading": self.moreInformation(nursing_grading)
		}

		return content

	def main(self):
		pageno = 222
		self.download(pageno)
		csvfile = file('directions.csv', 'rb')
		reader = csv.reader(csvfile)
		table = "directions"
		for line in reader:
			print "=="*40 + "\n正在解析第" + line[0] + "条"
			my_dict = self.structure(line)
			for k, v in my_dict.items():
				if v == None:
					my_dict.pop(k)
			self.insertData(table, my_dict)

if __name__ == "__main__":
	direction = DrugDirection()
	direction.main()
