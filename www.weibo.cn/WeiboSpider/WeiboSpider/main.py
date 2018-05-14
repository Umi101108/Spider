# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2018/5/13 下午5:36'

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.search import WeiboSpider


process = CrawlerProcess(get_project_settings())

process.crawl(WeiboSpider)
process.start()