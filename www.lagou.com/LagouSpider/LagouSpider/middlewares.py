# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2017/8/15 下午8:38'


class RandomUserAgentMiddleware(object):
    """This middleware allows spiders to override the user_agent"""

    def __init__(self, user_agent='Scrapy'):
        self.user_agent = user_agent



    def process_request(self, request, spider):
        ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        request.headers.setdefault("User-Agent", ua)