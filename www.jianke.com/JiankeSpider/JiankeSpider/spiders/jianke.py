# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request


class JiankeSpider(scrapy.Spider):
    name = 'jianke'
    allowed_domains = ['jianke.com']
    start_urls = ['http://jianke.com/']

    base_url = 'http://www.jianke.com/product/{}.html'

    def start_requests(self):
        for i in xrange(1, 2):
            url = self.base_url.format(str(i))
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # html = response.text
        # print html
        direction = response.css('#b_2_2').extract_first()
        print direction
        results = re.findall('<p>.*?<em>(.*?)</em>(.*?)</p>', direction, re.S)
        commonname = re.findall(u'通用名称：(.*?)</p> ', direction, re.S)
        tradename = re.findall(u'商品名称：(.*?)</p> ', direction, re.S)
        print commonname[0], tradename[0]
        raw = {}
        for r in results:
            print r[0], r[1]
            raw[r[0]] = r[1]
        commonname
        tradename
        ingredients = raw.get('', '')
        characters
        indications
        specification
        dosageandadministration
        adversereactions
        contraindications
        cautions
        list_interaction
        storage
        package
        usefullife
        implementstandard
        approvalno
        corporationname
        pass
