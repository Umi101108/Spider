# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2017/8/15 下午8:38'

from scrapy import signals

class RandomUserAgentMiddleware(object):
    """This middleware allows spiders to override the user_agent"""

    def __init__(self, user_agent='Scrapy'):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['USER-AGENT'])
        crawler.

    def process_request(self, request, spider):
        ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        request.headers.setdefault("User-Agent", ua)


class RandomProxyMiddleware(object):
    # 动态设置ip代理
    def process_request(self, request, spider):
        request.meta["proxy"] = "http://111.198.219.151:8118"