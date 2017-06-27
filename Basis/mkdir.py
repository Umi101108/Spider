# coding: utf-8
import os

pwd = 'D:\\pictures\\' or '/User/umi/pictures/'

def mkdir(self, path):
	path = path.strip()
	isExists = os.path.exists(os.path.join(pwd, path))
	if not isExists:
		print "新建了一个名为" + path + "的文件夹"
		os.makedirs(os.path.join(pwd, path))
		return True
	else:
		print "名字叫做" + path + "的文件夹已经存在了"
		return True