# -*- coding: utf-8 -*-

import datetime
import time

def createMarkdown(date, filename):
	with open(filename, 'w') as f:
		f.write("### " + date + "\n")

strdate = datetime.datetime.now().strftime('%Y-%m-%d')
filename = '{date}.md'.format(date=strdate)
createMarkdown(strdate, filename)


language = 'python'
title = 'getsploit'
url = 'https://github.com/vulnersCom/getsploit'
description = 'Command line utility for searching and downloading exploits'
with open(filename, 'a') as f:
	f.write('\n#### {language}'.format(language=language))
	f.write('\n* [{title}]({url}): \n{description}'.format(title=title, url=url, description=description))


