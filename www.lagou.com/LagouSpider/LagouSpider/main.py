# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2017/8/14 下午11:02'

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "lagou"])