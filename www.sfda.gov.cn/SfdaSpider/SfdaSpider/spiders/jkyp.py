# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from SfdaSpider.items import JkypItem


class JkypSpider(scrapy.Spider):
    name = 'jkyp'
    allowed_domains = ['http://qy1.sfda.gov.cn/']
    start_urls = ['http://qy1.sfda.gov.cn/']
    base_url = 'http://qy1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=36&tableName=TABLE36&tableView=%BD%F8%BF%DA%D2%A9%C6%B7&Id={}'
    def start_requests(self):
        for i in xrange(16201, 22000): #12370
            url = self.base_url.format(str(i))
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        html = response.text
        # print html
        results = re.findall('<tr>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?</tr>', html, re.S)
        raw = {}
        for r in results:
            # print r[0], re.sub('<.*?>', '', r[1])
            raw[r[0]] = re.sub('<.*?>', '', r[1])
        item = JkypItem()
        item["passno"] = raw.get(u'注册证号', '')
        item["passnoreg0"] = raw.get(u'原注册证号', '')
        item["packpassnoapp"] = raw.get(u'分包装批准文号', '')
        item["firmname"] = raw.get(u'公司名称（中文）', '')
        item["firmnameen"] = raw.get(u'公司名称（英文）', '')
        item["firmaddr"] = raw.get(u'地址（中文）', '')
        item["firmaddren"] = raw.get(u'地址（英文）', '')
        item["firmcountry"] = raw.get(u'国家/地区（中文）', '')
        item["firmcountryen"] = raw.get(u'国家/地区（英文）', '')
        item["commonname"] = raw.get(u'产品名称（中文）', '')
        item["englishname"] = raw.get(u'产品名称（英文）', '')
        item["tradename"] = raw.get(u'商品名（中文）', '')
        item["englishname2"] = raw.get(u'商品名（英文）', '')
        item["dosageform"] = raw.get(u'剂型（中文）', '')
        item["specs"] = raw.get(u'规格（中文）', '')
        item["packspecs"] = raw.get(u'包装规格（中文）', '')
        item["factory"] = raw.get(u'生产厂商（中文）', '')
        item["factoryen"] = raw.get(u'生产厂商（英文）', '')
        item["factoryaddr"] = raw.get(u'厂商地址（中文）', '')
        item["factoryaddren"] = raw.get(u'厂商地址（英文）', '')
        item["factorycountry"] = raw.get(u'厂商国家/地区（中文）', '')
        item["factorycountryen"] = raw.get(u'厂商国家/地区（英文）', '')
        item["approvaldate"] = raw.get(u'发证日期', '')
        item["closingdate"] = raw.get(u'有效期截止日', '')
        item["packfirmname"] = raw.get(u'分包装企业名称', '')
        item["packfirmaddr"] = raw.get(u'分包装企业地址', '')
        item["category"] = raw.get(u'产品类别', '')
        item["standardcd0"] = raw.get(u'药品本位码', '')
        item["standardcdrmk"] = raw.get(u'药品本位码备注', '')
        yield item
        pass
