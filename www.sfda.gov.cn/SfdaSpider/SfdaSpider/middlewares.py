# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2017/11/1 下午9:40'

import time
import random
from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from scrapy.xlib.pydispatch import dispatcher
from settings import DRIVER_PATH_C, DRIVER_PATH_P
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


from scrapy.signalmanager import SignalManager
from scrapy.responsetypes import responsetypes
from six.moves import queue
from twisted.internet import defer, threads
from twisted.python.failure import Failure

from utils.crawl_xici_ip import GetIP

class JSPageMiddleware(object):

    def __init__(self):
        # dcap =dict(DesiredCapabilities.CHROME)
        # dcap['']
        # self.chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(DRIVER_PATH_C)
        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap["phantomjs.page.settings.userAgent"] = (
        #     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
        # )
        # self.driver = webdriver.PhantomJS(DRIVER_PATH_P, desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any', '--web-security=false'])
        # self.driver.set_window_size(2000, 1500)
        super(JSPageMiddleware, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    # 通过chrome请求动态网页
    def process_request(self, request, spider):
        if spider.name == "gcyp":
            # driver = webdriver.Chrome("/Users/umi/Downloads/chromedriver")
            print "访问：{0}".format(request.url)
            self.driver.get(request.url)
            time.sleep(random.randint(2,5))
            if self.driver.page_source == '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body></body></html>':
                self.driver.quit()
                self.driver = webdriver.Chrome(DRIVER_PATH_C)
                print "重新访问：{0}".format(request.url)
                self.driver.get(request.url)
                time.sleep(random.randint(2,5))
            self.driver.save_screenshot('1.png')
            return HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding="utf-8", request=request)
        elif spider.name == "whatismyip":
            print "访问：{0}".format(request.url)
            # ip = GetIP().get_random_ip()
            ip = '183.190.26.154:80'
            print ip
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=http://%s' % ip)
            driver = webdriver.Chrome(DRIVER_PATH_C, chrome_options=chrome_options)
            driver.get(request.url)
            time.sleep(random.randint(2,5))
            return HtmlResponse(url=driver.current_url, body=driver.page_source, encoding="utf-8", request=request)


    def spider_closed(self, spider):
        # 当爬虫退出的时候关闭chrome
        print "spider closed"
        self.driver.quit()


# class PhantomJSDownloadHandler(object):
#
#     def __init__(self, settings):
#         self.options = settings.get('PHANTOMJS_OPTIONS', {})
#
#         max_run = settings.get('PHANTOMJS_MAXRUN', 10)
#         self.sem = defer.DeferredSemaphore(max_run)
#         self.queue = queue.LifoQueue(max_run)
#
#         SignalManager(dispatcher.Any).connect(self._close, signal=signals.spider_closed)
#
#     def download_request(self, request, spider):
#         """use semaphore to guard a phantomjs pool"""
#         return self.sem.run(self._wait_request, request, spider)
#
#     def _wait_request(self, request, spider):
#         try:
#             driver = self.queue.get_nowait()
#         except queue.Empty:
#             driver = webdriver.PhantomJS(**self.options)
#
#         driver.get(request.url)
#         # ghostdriver won't response when switch window until page is loaded
#         dfd = threads.deferToThread(lambda: driver.switch_to.window(driver.current_window_handle))
#         dfd.addCallback(self._response, driver, spider)
#         return dfd
#
#     def _response(self, _, driver, spider):
#         body = driver.execute_script("return document.documentElement.innerHTML")
#         if body.startswith("<head></head>"):  # cannot access response header in Selenium
#             body = driver.execute_script("return document.documentElement.textContent")
#         url = driver.current_url
#         respcls = responsetypes.from_args(url=url, body=body[:100].encode('utf8'))
#         resp = respcls(url=url, body=body, encoding="utf-8")
#
#         response_failed = getattr(spider, "response_failed", None)
#         if response_failed and callable(response_failed) and response_failed(resp, driver):
#             driver.close()
#             return defer.fail(Failure())
#         else:
#             self.queue.put(driver)
#             return defer.succeed(resp)
#
#     def _close(self):
#         while not self.queue.empty():
#             driver = self.queue.get_nowait()
#             driver.close()