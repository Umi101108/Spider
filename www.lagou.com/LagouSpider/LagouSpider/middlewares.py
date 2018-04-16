# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2017/8/15 下午8:38'

from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from scrapy.xlib.pydispatch import dispatcher
from fake_useragent import UserAgent

from LagouSpider.utils.crawl_xici_ip import GetIP


class UserAgentMiddleware(object):
    """This middleware allows spiders to override the user_agent"""

    def __init__(self, user_agent='Scrapy'):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['USER-AGENT'])
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self.user_agent = getattr(spider, 'user_agent', self.user_agent)

    def process_request(self, request, spider):
        # ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        # request.headers.setdefault("User-Agent", ua)
        if self.user_agent:
            request.headers.setdefault("User-Agent", self.user_agent)


class RandomUserAgentMiddleware(object):
    # 随机更换user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())


class RandomProxyMiddleware(object):
    # 动态设置ip代理
    def process_request(self, request, spider):
        # request.meta["proxy"] = "http://111.198.219.151:8118"
        get_ip = GetIP()
        request.meta["proxy"] = get_ip.get_random_ip()


class JSPageMiddleware(object):

    def __init__(self):
        self.driver = webdriver.Chrome("/Users/umi/Downloads/chromedriver")
        super(JSPageMiddleware, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    # 通过chrome请求动态网页
    def process_request(self, request, spider):
        if spider.name == "lagou":
            # driver = webdriver.Chrome("/Users/umi/Downloads/chromedriver")
            self.driver.get(request.url)
            import time
            time.sleep(3)
            print "访问：{0}".format(request.url)

            return HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding="utf-8", request=request)

    def spider_closed(self, spider):
        # 当爬虫退出的时候关闭chrome
        print "spider closed"
        self.driver.quit()


# todo
# scrapy-splash 支持分布式
# pyvirtualdisplay 无界面环境下运行chrome
#         from pyvirtualdisplay import Display
#         display = Display(visible=0, size=(800, 600))
#         display.start()
# selenium grid
# splinter