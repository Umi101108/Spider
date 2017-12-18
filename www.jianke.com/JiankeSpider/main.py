# -*- coding: utf-8 -*-

import sys
import os

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
command = "scrapy crawl jianke".split()
# command = "scrapy crawl whatismyip".split()
execute(command)