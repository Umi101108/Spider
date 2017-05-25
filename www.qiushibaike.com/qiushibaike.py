# -*- coding: utf-8 -*-

import sys
sys.path.append("..")

from Basis.strong_spider import Spider


print 2
spider = Spider()
print spider.get_html('http://www.baidu.com')