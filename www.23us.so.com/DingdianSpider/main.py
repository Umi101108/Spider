# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2017/9/13 下午9:24'

import sys
import os

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "dingdian"])