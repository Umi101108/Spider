# -*- coding: utf-8 -*-
import scrapy


class JkypSpider(scrapy.Spider):
    name = 'jkyp'
    allowed_domains = ['http://qy1.sfda.gov.cn/']
    start_urls = ['http://http://qy1.sfda.gov.cn//']

    def parse(self, response):
        pass
