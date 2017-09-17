# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from MzituSpider.items import MzituspiderItem


class MzituSpider(CrawlSpider):
    name = 'mzitu'
    allowed_domains = ['www.mzitu.com']
    start_urls = ['http://www.mzitu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'http://www.mzitu.com/\d{1,6}', deny=r'http://www.mzitu.com/\d{1,6}/\d{1,6}'), callback='parse_item', follow=True),
    )
    img_urls = []

    def parse_item(self, response):
        # item = MzituspiderItem()
        title = response.css('.main-title::text').extract_first()

        # item["title"] = title
        # item["url"] = response.url

        max_pageno = response.css('.pagenavi span::text').extract()[-2]
        print title, max_pageno, response.url
        for pageno in xrange(1, int(max_pageno)+1):
            page_url = response.url + '/' + str(pageno)
            yield Request(url=page_url, callback=self.img_url, meta={"title": title, "url": response.url})


    def img_url(self, response):
        img_urls = response.css('.main-image img::attr(src)').extract()
        for img_url in img_urls:
            self.img_urls.append(img_url)
            print img_url
        item = MzituspiderItem()
        item["title"] = response.meta["title"]
        item["url"] = response.meta["url"]
        item["image_urls"] = self.img_urls
        yield item

