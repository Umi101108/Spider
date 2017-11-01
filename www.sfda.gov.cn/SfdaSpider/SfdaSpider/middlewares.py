# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2017/11/1 下午9:40'

import time
from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from scrapy.xlib.pydispatch import dispatcher


class JSPageMiddleware(object):

    def __init__(self):
        self.driver = webdriver.Chrome("/Users/umi/Downloads/chromedriver")
        # self.driver = webdriver.PhantomJS("/Users/umi/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs")
        super(JSPageMiddleware, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    # 通过chrome请求动态网页
    def process_request(self, request, spider):
        if spider.name == "gcyp":
            # driver = webdriver.Chrome("/Users/umi/Downloads/chromedriver")
            self.driver.get(request.url)
            time.sleep(10)
            print "访问：{0}".format(request.url)

            return HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding="utf-8", request=request)

    def spider_closed(self, spider):
        # 当爬虫退出的时候关闭chrome
        print "spider closed"
        self.driver.quit()