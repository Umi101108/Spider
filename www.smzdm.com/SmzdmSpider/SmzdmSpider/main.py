# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2017/8/23 下午10:44'

import sys
import os

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "smzdm_master"])
execute(["scrapy", "crawl", "smzdm"])