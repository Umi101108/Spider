# -*- coding: utf-8 -*-
import re
from urlparse import urljoin
import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = (
        'http://blog.jobbole.com/all-posts/',
    )

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
            print image_url, post_url
            image_url = urljoin("http://blog.jobbole.com/", image_url)
            # print urlparse(response.url, post_url)

            yield Request(url=post_url, meta={"front_image_url": image_url}, callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载
        next_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_url:
            yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        article_item = JobBoleArticleItem()

        # 通过xpath提取文章的具体字段
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract_first().replace(u"·","").strip()
        # praise_nums = response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract_first()
        # fav_nums = response.xpath('//span[contains(@class, "bookmark-btn")]/text()').extract_first()
        # # fav_nums = re.sub('\D', '', fav_nums)
        # match_re = re.match(".*?(\d+).*?", fav_nums)
        # if match_re:
        #     fav_nums = match_re.group(1)
        # comment_nums = response.xpath('//a[@href="#article-comment"]/span/text()').extract_first()
        # comment_nums = re.sub('\D', '', comment_nums)
        # content = response.xpath('//div[@class="entry"]').extract_first()
        # tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith(u'评论')]
        # tag = ','.join(tag_list)

        # 通过css选择器提取字段
        # title = response.css(".entry-header h1::text").extract_first('')
        # front_image_url = response.meta.get("front_image_url", "")
        # create_date = response.css("p.entry-meta-hide-on-mobile::text").extract_first('').replace(u"·","").strip()
        # praise_nums = response.css(".vote-post-up h10::text").extract_first('')
        # fav_nums = response.css(".bookmark-btn::text").extract_first('')
        # fav_nums = re.sub('\D', '', fav_nums)
        # comment_nums = response.css("a[href='#article-comment'] span::text").extract_first('')
        # comment_nums = re.sub('\D', '', comment_nums)
        # content = response.css('div.entry').extract_first()
        # tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith(u'评论')]
        # tags = ','.join(tag_list)
        #
        # article_item["title"] = title
        # article_item["url"] = response.url
        # article_item["url_object_id"] = get_md5(response.url)
        # article_item["create_date"] = create_date
        # article_item["front_image_url"] = [front_image_url]
        # article_item["praise_nums"] = praise_nums
        # article_item["comment_nums"] = comment_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["tags"] = tags
        # article_item["content"] = content

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
