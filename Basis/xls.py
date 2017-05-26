# -*- coding: utf-8 -*-

import xlwt

newTable = 'table.xls'
wb = xlwt.Workbook(encoding='utf-8')
ws = wb.add_sheet('sheet1')
ws.write(0, 2, ['col1'], xlwt.easyxf('font: bold on'))  # 行 列 数据
wb.save(newTable)