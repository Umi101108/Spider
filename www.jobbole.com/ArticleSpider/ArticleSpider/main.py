# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2017/8/6 下午2:13'

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "jobbole_master"])