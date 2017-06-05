# -*- coding: utf-8 -*-

import xlwt  # 写模块
import xlrd  # 读模块

# read 
wb = xlrd.open_workbook('table.xls')
sheet = wb.sheets()[0]
for i in range(5):
	if i == 0:
		continue
	str = sheet.row_values(i)[2]
	print str

# write
newTable = 'table.xls'
wb = xlwt.Workbook(encoding='utf-8')
ws = wb.add_sheet('sheet1')
for i in range(10):
	ws.write(i, 2, ['col1'], xlwt.easyxf('font: bold on'))  # 行 列 数据
wb.save(newTable)