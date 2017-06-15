# coding: utf-8

import csv
import re
import MySQLdb

class Guidance(object):
	def __init__(self):
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
			print "数据库连接错误，原因%d: %s" % (e.args[0], e.args[1])

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


	def structure(self, line):

		text = line[5].encode('utf8').strip()+'【'

		zhuyaoyongtu_pattern = re.compile(r'【主要用途】(.*?)【', re.S)
		zyyt = re.match(zhuyaoyongtu_pattern, text)
		if zyyt:
			# print '主要用途: ' + zyyt.group(1)
			mainuses = zyyt.group(1)
		else:
			mainuses = ''

		rhshgy_pattern = re.compile(r'【如何使用该药】(.*?)【', re.S)
		rhshgy = re.search(rhshgy_pattern, text)
		if rhshgy:
			# print '如何使用该药：' + rhshgy.group(1)
			drugusage = rhshgy.group(1)
		else:
			drugusage = ''

		xjcdcs_pattern = re.compile(r'【需监测的参数】(.*?)【', re.S)
		xjcdcs = re.search(xjcdcs_pattern, text)
		if xjcdcs:
			# print '需监测的参数: ' + xjcdcs.group(1)
			parameter = xjcdcs.group(1)
		else:
			parameter = ''

		yyhkncxdbszz_pattern = re.compile(r'【用药后可能出现的不适症状】(.*?)【', re.S)
		yyhkncxdbszz = re.search(yyhkncxdbszz_pattern, text)
		if yyhkncxdbszz:
			# print '用药后可能出现的不适症状: ' + yyhkncxdbszz.group(1)
			symptom = yyhkncxdbszz.group(1)
		else:
			symptom = ''

		yzjg_pattern = re.compile(r'【严重警告】(.*?)【', re.S)
		yzjg = re.search(yzjg_pattern, text)
		if yzjg:
			# print '严重警告: ' + yzjg.group(1)
			seriouswarning = yzjg.group(1)
		else:
			seriouswarning = ''

		cyjl_pattern = re.compile(r'【常用剂量】(.*?)【', re.S)
		cyjl = re.search(cyjl_pattern, text)
		if cyjl:
			# print '常用剂量: ' + cyjl.group(1)
			commondose = cyjl.group(1)
		else:
			commondose = ''

		qxsjhwcsj_pattern = re.compile(r'【起效时间和维持时间】(.*?)【', re.S)
		qxsjhwcsj = re.search(qxsjhwcsj_pattern, text)
		if qxsjhwcsj:
			# print '起效时间和维持时间: ' + qxsjhwcsj.group(1)
			drugtime = qxsjhwcsj.group(1)
		else:
			drugtime = ''

		tsrqyyzd_pattern = re.compile(r'【特殊人群用药指导】(.*?)【', re.S)
		tsrqyyzd = re.search(tsrqyyzd_pattern, text)
		if tsrqyyzd:
			# print '特殊人群用药指导: ' + tsrqyyzd.group(1)
			specialguidance = tsrqyyzd.group(1)
		else:
			specialguidance = ''

		bq_pattern = re.compile(r'【标签】(.*?)【', re.S)
		bq = re.search(bq_pattern, text)
		if bq:
			# print '标签: ' + bq.group(1)
			druglabel = bq.group(1)
		else:
			druglabel = ''

		ylcyydywxhzy_pattern = re.compile(r'【有临床意义的药物相互作用】(.*?)【', re.S)
		ylcyydywxhzy = re.search(ylcyydywxhzy_pattern, text)
		if ylcyydywxhzy:
			print '有临床意义的药物相互作用: ' + ylcyydywxhzy.group(1)
			druginteraction = ylcyydywxhzy.group(1)
		else:
			druginteraction = ''

		rhbcyp_pattern = re.compile(r'【如何保存药品】(.*?)【', re.S)
		rhbcyp = re.search(rhbcyp_pattern, text)
		if rhbcyp:
			# print '如何保存药品: ' + rhbcyp.group(1)
			storage = rhbcyp.group(1)
		else:
			storage = ''

		bztd_pattern = re.compile(r'【辨证特点】(.*?)【', re.S)
		bztd = re.search(bztd_pattern, text)
		if bztd:
			# print '辨证特点: ' + bztd.group(1)
			clinicfeatures = bztd.group(1)
		else:
			clinicfeatures =''

		content = {
			"drugno": line[1],
			"mainuses": mainuses,
			"drugusage": drugusage,
			"parameter": parameter,
			"symptom": symptom,
			"seriouswarning": seriouswarning,
			"commondose": commondose,
			"drugtime": drugtime,
			"specialguidance": specialguidance,
			"druglabel": druglabel,
			"druginteraction": druginteraction,
			"storage": storage,
			"clinicfeatures": clinicfeatures,
		}
		return content

	def main(self):
		csvfile = file('d:/0615.csv', 'rb')
		reader = csv.reader(csvfile)
		table = "bc_drug_guidancedb"
		for line in reader:
			# print line[0], line[1], line[2], line[3].encode('utf8'), line[4].encode('utf8'), line[5].encode('utf8')
			if line[5]!='':
				my_dict = self.structure(line)
				# for k, v in content.items():
				# 	print k, v
				self.insertData(table, my_dict)


if __name__ == "__main__":
	guidance = Guidance()
	guidance.main()