# -*- coding: utf-8 -*-

import csv


with open('filename', 'rb') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		print row

with open('filename', 'w') as csvfile:
	writer = csv.writer(csvfile, dialect = 'excel')
	writer.writerow([('col1', 'col2', 'col3')])
	items = [
			('xiaoming', 'china', '10'),
			('lina', 'USA', '12')
		]
	for item in items:
		writer.writerow([tuple(item).encode('utf8')])