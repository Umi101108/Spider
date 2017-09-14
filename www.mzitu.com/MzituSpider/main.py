# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2017/9/14 下午9:32'

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "mzitu"])