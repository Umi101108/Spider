# -*- coding: utf-8 -*-

import MySQLdb

connect = MySQLdb.connect(
	host = 'localhost',
	user = 'root',
	passwd = 'gt123456',
	db = 'world',
	port = 3306,
	charset = 'utf8',
	)

cursor = connect.cursor()
sql = "select * from country where Name like 'a%'; "
column = []

try:
	cursor.execute(sql)
	for desc in cursor.description:
		column.append(desc[0])
	print column
	results = cursor.fetchall()
	for r in results:
		print list(r)
	connect.commit()
except:
	print "Error"
	connect.rollback()


cursor.close()
connect.close()