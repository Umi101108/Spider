# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from SfdaSpider.items import GcypItem

class GcypSpider(scrapy.Spider):
    name = "gcyp"
    allowed_domains = ["qy1.sfda.gov.cn"]
    start_urls = (
        'http://qy1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=25&tableName=TABLE25&tableView=%B9%FA%B2%FA%D2%A9%C6%B7&Id=11881',
        # 'http://www.jianshu.com/p/9ff03b41c184',
    )
    base_url = 'http://qy1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=25&tableName=TABLE25&tableView=%B9%FA%B2%FA%D2%A9%C6%B7&Id={}'

    def start_requests(self):
        for i in xrange(24000, 80000):
            url = self.base_url.format(str(i))
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        html = response.text
        print html
        results = re.findall('<tr>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?</tr>', html, re.S)
        raw = {}
        for r in results:
            # print r[0], re.sub('<.*?>', '', r[1])
            raw[r[0]] = re.sub('<.*?>', '', r[1])
        item = GcypItem()
        item["passno"] = raw.get(u'批准文号', '')
        item["commonname"] = raw.get(u'产品名称', '')
        item["englishname"] = raw.get(u'英文名称', '')
        item["tradename"] = raw.get(u'商品名', '')
        item["dosageform"] = raw.get(u'剂型', '')
        item["specs"] = raw.get(u'规格', '')
        item["factory"] = raw.get(u'生产单位', '')
        item["factoryaddr"] = raw.get(u'生产地址', '')
        item["sort"] = raw.get(u'产品类别', '')
        item["approvaldate"] = raw.get(u'批准日期', '')
        item["passnoreg0"] = raw.get(u'原批准文号', '')
        item["standardcd0"] = raw.get(u'药品本位码', '')
        item["standardcdrmk"] = raw.get(u'药品本位码备注', '')
        yield item
        # print item
        pass
