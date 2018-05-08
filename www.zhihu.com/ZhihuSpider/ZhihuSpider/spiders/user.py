# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Spider, Request, FormRequest
from ZhihuSpider.items import UserItem


class UserSpider(scrapy.Spider):
    name = 'user'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    start_user = 'excited-vczh'

    # user_url = 'https://www.zhihu.com/api/v4/members/muwriter?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
    # url = 'https://www.zhihu.com/api/v4/members/lun-zi-ge/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
    followees_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    followees_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Host': 'www.zhihu.com',
    }

    # custom_settings = {
    #     "COOKIES_ENABLED": True,
    #     "COOKIES_DEBUG": True,
    # }
    cookie = {'q_c1': '1636fc85ede4412c99223a865f64356c|1523620140000|1523620140000', 'zap': 'fceb8cfd-b412-44e3-98d2-06d082a8c292', 'l_cap_id': '"MjQwMTZhMTQ0ZTBmNDEzZWJkMjRlZTM0MzNmODk4NTY=|1523708283|7c0559df9ec1724166bfbfa6ecea16d573c1c55d"', 'r_cap_id': '"YTY5ZjZkNDVlMWVjNDk3NWFhZjJjYWZkNjYwZWYzMjQ=|1523708283|791db54a00fefa8d9580319e2c7cd58c30b6e9b0"', 'cap_id': '"ZTQ0NjRlODM1MGYyNGZmMDgzOWRkZTI1MGIwZWNmYWM=|1523708283|d47f3d7c4133153628a469cdf068579163433f56"', '__utma': '51854390.521600280.1523708288.1523708288.1523708288.1', '__utmz': '51854390.1523708288.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)', '__utmv': '51854390.000--|3=entry_date=20180414=1', 'capsion_ticket': '"2|1:0|10:1525276219|14:capsion_ticket|44:OTc5OWNjY2RkMTMyNDQ1MWE3MWEwZjhmNzVhN2RjOTI=|6c626866459b12f53dfe65fd8e1809cf53550a82a37e610c983f997ccf3703b4"', 'z_c0': '"2|1:0|10:1525276226|4:z_c0|80:MS4xMjNKU0FBQUFBQUFtQUFBQVlBSlZUVUlzMTF0dnJPUU5mVTVpVWpqclItSTlOQm1vVkhMSDl3PT0=|e1b11a3ce0ba26d8b418d68b6dca12ffb934c638c8e248c03cd3300bc85fad17"', 'd_c0': '"AJAueLh2iA2PTmgDfU6fOtRO7G-9zQ9JVj8=|1525276226"', 'aliyungf_tc': 'AQAAADZhKF44NQMAlxBOfF2Xy4yev/dn', '_xsrf': '5005b42c-0005-4692-80db-7861d4ef334b',}

    def start_requests(self):
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), headers=self.headers, callback=self.parse_user, cookies=self.cookie)
        yield Request(self.followees_url.format(user=self.start_user, include=self.followees_query, offset=0, limit=20), headers=self.headers, callback=self.parse_followees, cookies=self.cookie)
        yield Request(self.followers_url.format(user=self.start_user, include=self.followers_query, offset=0, limit=20), headers=self.headers, callback=self.parse_followers, cookies=self.cookie)

        # yield Request(url, headers=self.headers, callback=self.parse, cookies=self.cookie)


    def parse(self, response):
        print (response.request.headers)
        print (response.encoding)
        print (type(response.text))
        print (response.text)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item

        yield Request(self.followees_url.format(user=result.get('url_token'), include=self.followees_query, limit=20, offset=0), callback=self.parse_followees)
        yield Request(self.followees_url.format(user=result.get('url_token'), include=self.followees_query, limit=20, offset=0), callback=self.parse_followers)

    def parse_followees(self, response):
        results = json.loads(response.text)
        print (results)
        if 'data' in results.keys():
            for result in results.get('data'):
                print (result.get('url_token'))
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query), callback=self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            yield Request(results.get('paging').get('next'), callback=self.parse_followees)

    def parse_followers(self, response):
        results = json.loads(response.text)
        print (results)
        if 'data' in results.keys():
            for result in results.get('data'):
                print (result.get('url_token'))
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query), callback=self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            yield Request(results.get('paging').get('next'), callback=self.parse_followers)