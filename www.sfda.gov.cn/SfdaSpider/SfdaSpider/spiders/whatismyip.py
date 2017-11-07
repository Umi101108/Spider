# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class WhatismyipSpider(scrapy.Spider):
    name = 'whatismyip'
    allowed_domains = ['whatismyip.com.tw']
    start_urls = ['http://www.whatismyip.com.tw/']

    def start_requests(self):
        for i in xrange(1, 100):
            yield Request(url=self.start_urls[0], callback=self.parse, dont_filter=True)

    def parse(self, response):
        html = response.text
        print html