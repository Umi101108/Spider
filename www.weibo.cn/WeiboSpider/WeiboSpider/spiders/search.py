# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, FormRequest
from items import WeibospiderItem

class WeiboSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['weibo.cn']
    # search_url = 'https://weibo.cn/search/?pos=search'
    search_url = 'https://weibo.cn/search/mblog'
    max_page = 10
    keywords = ['宋伊人']

    cookies_raw = '_T_WM=62eda214392f0618f0336346688098e1; SCF=AvwzagndiVhyirA4jY0sUyhXy-MvVy1I4w5ONswfyeMIyRfcqhqztNeYJNlMgBIRq89auZKvbyan-p9nGudzKC4.; TMPTOKEN=gPQFmY1dMFRosvESoCnMSHfIMooOqDqAquIRQlUzSSapSoIzhWPNtHvONrifYO1Q; SUB=_2A253_F0yDeRhGedJ7FER8CjIwj6IHXVVH2N6rDV6PUJbkdB-LXaikW1NUbuWFET7hf1nfNkuffFohTZnay11mulj; SUHB=0ebsv81LVJMUZw; SSOLoginState=1526213986'
    cookies = {k.split('=')[0].strip(): k.split('=')[1].strip() for k in cookies_raw.split(';')}
    def start_requests(self):
        for keyword in self.keywords:
            url = '{url}?keyword={keyword}'.format(url=self.search_url, keyword=keyword)
            for page in range(self.max_page+1):
                url += '&page={page}'.format(page=str(page))
                data = {
                    'keyword': keyword,
                    'page': str(page),
                }
                yield FormRequest(url, callback=self.parse, formdata=data)

    def parse(self, response):
        weibos = response.xpath('//div[@class="c" and contains(@id, "M_")]')
        for weibo in weibos:
            is_forward = weibo.xpath('.//span[@class="cmt"]').extract_first()
            if is_forward:
                detail_url = weibo.xpath('.//a[contains(., "原文评论")]//@href').extract_first()
            else:
                detail_url = weibo.xpath('.//a[contains(., "评论")]//@href').extract_first()
            print (detail_url)
            yield Request(detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        url = response.url
        content = ''.join(response.xpath('//div[@id="M_"]//span[@class="ctt"]//text()').extract())
        id = response.url.split('?')[0].split('/')[-1]
        comment_count = response.xpath('//span[@class="pms"]//text()').re_first('评论\[(.*?)\]')
        forward_count = response.xpath('//a[contains(., "转发[")]//text()').re_first('转发\[(.*?)\]')
        like_count = response.xpath('//a[contains(., "赞[")]//text()').re_first('赞\[(.*?)\]')
        posted_at = response.xpath('//div[@id="M_"]//span[@class="ct"]//text()').extract_first('')
        user = response.xpath('//div[@id="M_"]/div[1]/a/text()').extract_first('')
        weibo_item = WeibospiderItem()
        for field in weibo_item.fields:
            try:
                weibo_item[field] = eval(field)
            except NameError:
                print ('Field is Not Defined', field)
        yield weibo_item