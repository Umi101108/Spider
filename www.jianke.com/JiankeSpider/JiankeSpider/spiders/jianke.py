# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from JiankeSpider.items import DrugItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class JiankeSpider(CrawlSpider):
    name = 'jianke'
    allowed_domains = ['jianke.com']
    start_urls = ['https://www.jianke.com/list-010301.html']

    base_url = 'https://www.jianke.com/product/{}.html'

    rules = (

        Rule(LinkExtractor(allow=("https://www.jianke.com/list-01\d{2,4}.html",)), follow=True),
        Rule(LinkExtractor(allow=("https://www.jianke.com/list-01\d{2,4}-0-\d{1,2}-0-1-0-0-0-0-0.html",)), follow=True),
        Rule(LinkExtractor(allow=r'https://www.jianke.com/product/\d+.html'), callback='parse_drug', follow=True),
    )

    # def start_requests(self):
    #     for i in xrange(10000, 20000):
    #         url = self.base_url.format(str(i))
    #         yield Request(url=url, callback=self.parse)


    def parse_drug(self, response):
        direction = response.css('#b_2_2').extract_first()
        results = re.findall('<p>.*?<em>(.*?)</em>(.*?)</p>', direction, re.S)
        commonname = re.findall(u'通用名称：(.*?)</p>', direction, re.S)
        tradename = re.findall(u'商品名称：(.*?)</p>', direction, re.S)
        raw = {}
        for r in results:
            raw[re.sub(u'【|】| ', '', r[0])]=r[1]

        item = DrugItem()
        item["productid"] = response.url.split('/')[-1].split('.')[0]
        item['commonname'] = ''.join(commonname)
        item['tradename'] = ''.join(tradename)
        item['warningsmarks'] = raw.get(u'警示语', '')
        item['ingredients'] = raw.get(u'主要成份', '')
        item['characters'] = raw.get(u'性状', '')
        item['radioactivityandtime'] = raw.get(u'放射性活度和标识时间', '')
        item['actioncategory'] = raw.get(u'作用类别', '')
        item['indications'] = raw.get(u'适应症/功能主治', '')
        item['specification'] = raw.get(u'规格型号', '')
        item['dosageandadministration'] = raw.get(u'用法用量', '')
        item['adversereactions'] = raw.get(u'不良反应', '')
        item['contraindications'] = raw.get(u'禁忌', '')
        item['warning'] = raw.get(u'警告', '')
        item['cautions'] = raw.get(u'注意事项', '')
        item['pregnancyandnursingmothers'] = raw.get(u'孕妇及哺乳期妇女用药', '')
        item['pediatricuse'] = raw.get(u'儿童用药', '')
        item['geriatricuse'] = raw.get(u'老年患者用药', '')
        item['list_interaction'] = raw.get(u'药物相互作用', '')
        item['overdosage'] = raw.get(u'药物过量', '')
        item['clinicaltrails'] = raw.get(u'临床试验', '')
        item['pharmacologicalandtoxicological'] = raw.get(u'药理毒理', '')
        item['pharmacokinetics'] = raw.get(u'药代动力学', '')
        item['storage'] = raw.get(u'贮藏', '')
        item['package'] = raw.get(u'包装', '')
        item['usefullife'] = raw.get(u'有效期', '')
        item['implementstandard'] = raw.get(u'执行标准', '')
        item['approvalno'] = raw.get(u'批准文号', '')
        item['registerno'] = raw.get(u'进口药品注册证号', '')
        item['importlicenceno'] = raw.get(u'进口许可证号', '')
        item['corporationname'] = raw.get(u'生产企业', '')

        yield item