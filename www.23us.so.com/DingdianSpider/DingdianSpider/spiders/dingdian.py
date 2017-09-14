# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from DingdianSpider.items import DingdianItem, DingdianContentItem


class DingdianSpider(scrapy.Spider):
    name = 'dingdian'
    allowed_domains = ['www.23us.so']
    start_urls = ['http://www.23us.so/']
    base_url = 'http://www.23us.so/list/{}_{}.html'


    def start_requests(self):
        for i in xrange(1, 10):
            url = self.base_url.format(str(i), '1')
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        max_pageno = response.css('.pagelink a::text').extract()[-1]
        for pageno in xrange(1, int(max_pageno)+1):
            url = response.url.split('_')[0] + '_' + str(pageno) + '.html'
            yield Request(url=url, callback=self.get_name)

    def get_name(self, response):
        tr_list = response.css('tr[bgcolor="#FFFFFF"]')
        for tr in tr_list:
            name = tr.css('a::text').extract_first()
            novel_url = tr.css('a::attr(href)').extract_first()
            author = tr.css('td.C::text').extract()[0]
            serial_num = tr.css('td.R::text').extract_first()
            serial_status = tr.css('td.C::text').extract()[-1]

            yield Request(url=novel_url, callback=self.get_detail, meta={'name': name,
                                                                         'novel_url': novel_url,
                                                                         'author': author,
                                                                         'serial_num': serial_num,
                                                                         'serial_status': serial_status})

    def get_detail(self, response):
        category = response.css('tr td a::text').extract_first()
        article_url = response.css('.btnlinks a.read::attr(href)').extract_first()
        id = article_url.split('/')[-2]
        click_num = response.css('table[id="at"] tr')[2].css('td::text').extract_first()
        fav_num = response.css('table[id="at"] tr')[3].css('td::text').extract_first()
        item = DingdianItem()
        item["id"] = id
        item["name"] = response.meta['name']
        item["author"] = response.meta['author']
        item["category"] = category
        item["serial_num"] = response.meta['serial_num']
        item["serial_status"] = response.meta['serial_status']
        item["novel_url"] = response.url
        item["click_num"] = int(click_num)
        item["fav_num"] = int(fav_num)
        yield item
        yield Request(url=article_url, callback=self.get_chapter, meta={'id': id,
                                                                        'name': response.meta['name']})

    def get_chapter(self, response):
        td_list = response.css('table[id="at"] tr td')
        n = 0
        for td in td_list:
            n += 1
            chapter_url = td.css('a::attr(href)').extract_first()
            chapter_name = td.css('a::text').extract_first()
            yield Request(url=chapter_url, callback=self.get_chaptercontent, meta={'n': n,
                                                                                   'novel_id': response.meta['id'],
                                                                                   'name':response.meta['name'],
                                                                                   'chapter_url': chapter_url,
                                                                                   'chapter_name': chapter_name})

    def get_chaptercontent(self, response):
        content = response.css('dd#contents::text').extract()
        item = DingdianContentItem()
        item["novel_id"] = response.meta['novel_id']
        item["novel_name"] = response.meta['name']
        item["chapter_url"] = response.meta['chapter_url']
        item["chapter_name"] = response.meta['chapter_name']
        item["chapter_no"] = response.meta['n']
        item["content"] = ''.join(content)
        yield item
