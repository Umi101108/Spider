# -*- coding: utf-8 -*-

import csv

with open('filename', 'w') as csvfile:
	writer = csv.writer(csvfile, dialect = 'excel')
	writer.writerow([('col1', 'col2', 'col3')])
	for item in items:
		writer.writerow([tuple(item).encode('utf8')])