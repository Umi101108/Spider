# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2018/4/16 下午11:52'

import re
from redis import Redis
from urlparse import urljoin
import scrapy
from scrapy import Request
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy_redis.spiders import RedisSpider

from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5


identity = 'master'

class JobboleSpider(RedisSpider):
    name = "jobbole_master"
    allowed_domains = ["blog.jobbole.com"]
    if identity == 'master':
        r = Redis(host='host', port=port, password='password', decode_responses=True)
        url = 'http://blog.jobbole.com/all-posts/'
        r.lpush('jobbole:start_urls', url)


    redis_key = 'jobbole:start_urls'
    # 收集伯乐在线所有404的url以及404页面
    handle_httpstatus_list = [404, 301]

    def __init__(self):
        self.fail_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))
        pass


    def parse(self, response):
        """
        1. 获取文章列表页中的文章url并交给scrapy下载后并进行解析
        2. 获取下一页的url并交给scrapy进行下载，下载完成后交给parse
        """
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")

        # 解析列表页的所有文章url并交给scrapy下载后并进行解析
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first(" ")
            image_url = urljoin("http://blog.jobbole.com/", image_url)

            yield Request(url=post_url, meta={"front_image_url": image_url}, callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载
        next_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_url:
            yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        # 通过item_loader加载item
        front_image_url = response.meta.get("front_image_url", "")
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", front_image_url)
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")
        # 调用这个方法来对规则进行解析生成item对象
        article_item = item_loader.load_item()

        yield article_item