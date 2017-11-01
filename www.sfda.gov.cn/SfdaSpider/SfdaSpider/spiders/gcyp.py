# -*- coding: utf-8 -*-
import scrapy


class GcypSpider(scrapy.Spider):
    name = "gcyp"
    allowed_domains = ["qy1.sfda.gov.cn"]
    start_urls = (
        'http://qy1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=25&tableName=TABLE25&tableView=%B9%FA%B2%FA%D2%A9%C6%B7&Id=11881',
        # 'http://www.jianshu.com/p/9ff03b41c184',
    )

    def parse(self, response):
        print response.text
        pass
