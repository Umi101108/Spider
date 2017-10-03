# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy_redis.spiders import RedisCrawlSpider

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from SmzdmSpider.items import SmzdmspiderItemLoader, SmzdmArticleItem, SmzdmArticleContentItem, ArticleTagItem, CommentItem, MemberItem


class SlaveSpider(RedisCrawlSpider):
    name = 'smzdm_slave'
    allowed_domains = ['smzdm.com']
    # start_urls = ['http://www.smzdm.com/']
    # redis_key = 'smzdmSpider:start_urls'

    rules = (
        # Rule(LinkExtractor(allow=("fenlei/.*",)), follow=True),
        # Rule(LinkExtractor(allow=("baoliao/.*",)), follow=True),
        Rule(LinkExtractor(allow=r'www.smzdm.com/p/\d+/$'), callback='parse_post', follow=True),
        # Rule(LinkExtractor(allow=r'www.smzdm.com/p/\d+/p\d+/'), callback='parse_comment', follow=True),
        Rule(LinkExtractor(allow=r'zhiyou.smzdm.com/member/\d+/$'), callback='parse_member', follow=True),
    )

    def parse_post(self, response, follow=True):
        for article in self.parse_article(response):
            yield article
        if response.css('.comment_wrap'):
            for comment in self.parse_comment(response):
                yield comment


    def parse_article(self, response, follow=True):
        # 获取爆料内容
        match_obj = re.match(".*?www.smzdm.com/p/(\d+)/.*?", response.url)
        if match_obj:
            article_id = int(match_obj.group(1))

        item_loader = SmzdmspiderItemLoader(item=SmzdmArticleItem(), response=response)
        item_loader.add_value("article_id", article_id)
        item_loader.add_css("article_channel", '#article_channel::attr(value)')
        item_loader.add_css("article_title", '.article_title > em[itemprop="name"]::text')
        item_loader.add_value("article_url", response.url)
        if response.css('.ellipsis.author'):
            if response.css('.ellipsis.author > a::text'):
                ellipsis_author = response.css('.ellipsis.author > a::text').extract_first("None")
                ellipsis_author_id = response.css('.ellipsis.author > a::attr(href)').extract_first("None")
            else:
                ellipsis_author = "商家自荐"
                ellipsis_author_id = "商家自荐"
        else:
            ellipsis_author = "None"
            ellipsis_author_id = "None"
        item_loader.add_value("ellipsis_author", ellipsis_author)
        item_loader.add_value("ellipsis_author_id", ellipsis_author_id)
        item_loader.add_css("update_time", '.article_meta > span:last-child::text')
        price = response.css('em[itemprop="price"]::text').extract_first("0")
        item_loader.add_value("price", price)
        item_loader.add_css("price_currency", 'meta[itemprop="priceCurrency"]::attr(content)')
        item_loader.add_css("price_detail", 'em[itemprop="offers"] span.red::text')
        item_loader.add_css("buy_url", '.buy a::attr(href)')
        # item_loader.add_css("content", '.item-preferential')
        item_loader.add_css("fav_num", 'div.leftLayer > a.fav em::text')
        item_loader.add_css("comment_num", 'div.leftLayer > a.comment em::text')
        item_loader.add_css("rating_all_num", '#rating_all_num em::text')
        item_loader.add_css("rating_worthy_num", '#rating_worthy_num::text')
        item_loader.add_css("rating_unworthy_num", '#rating_unworthy_num::text')

        article_item = item_loader.load_item()
        yield article_item

        # item_loader2 = SmzdmspiderItemLoader(item=SmzdmArticleContentItem(), response=response)
        # item_loader2.add_value("article_id", article_id)
        # item_loader2.add_css("content", '.item-preferential')
        # article_content = item_loader2.load_item()
        # yield article_content

        # tags = response.css('span.tags div::text').extract()
        # tags = [tag.strip() for tag in tags if tag.strip()]
        # tags = ','.join(tags)

        tags = response.css('.meta-tags')
        for tag in tags:
            tag_item = ArticleTagItem()
            tag_url = tag.css('a::attr(href)').extract_first("")
            tag_detail = tag.css('a::text').extract_first("")
            tag_sort = tag.css('div div::text').extract_first("").split(u'：')[0] if tag.css('div div') else "暂无分类"

            tag_item["article_id"] = article_id
            tag_item["article_url"] = response.url
            tag_item["tag_sort"] = tag_sort
            tag_item["tag_detail"] = tag_detail
            yield tag_item


    def getTag(self, response, article_id):
        tags = response.css('.meta-tags')
        for tag in tags:
            tag_item = ArticleTagItem()
            tag_url = tag.css('a::attr(href)').extract_first("")
            tag_detail = tag.css('a::text').extract_first("")
            tag_sort = tag.css('div div::text').extract_first("").split(u'：')[0] if tag.css('div div') else "暂无分类"
            print tag_sort, tag_detail, tag_url

            tag_item["article_id"] = article_id
            tag_item["article_url"] = response.url
            tag_item["tag_sort"] = tag_sort
            tag_item["tag_detail"] = tag_detail
            yield tag_item


    def parse_comment(self, response, follow=True):
        comments = response.css("div#commentTabBlockNew ul.comment_listBox li.comment_list")
        match_obj = re.match(".*?www.smzdm.com/p/(\d+)/.*?", response.url)
        if match_obj:
            article_id = int(match_obj.group(1))
        for comment in comments:
            grey = comment.css('span::text').extract_first("")
            usmzdmid = comment.css('a.a_underline::attr(usmzdmid)').extract_first("")
            author = comment.css('span[itemprop="author"]::text').extract_first("")
            rank = comment.css('div.rank::attr(title)').extract_first("")
            comment_con = comment.css('div.comment_conWrap')[-1].css('div.comment_con span::text').extract_first("")
            time = comment.css('.time::text').extract_first("")
            come_from = comment.css('.come_from a::text').extract_first(" ")
            dingnum = comment.css('div.comment_action a.dingNum span::text').extract_first("")
            cainum = comment.css('div.comment_action a.caiNum span::text').extract_first("")

            # print grey, usmzdmid, author, rank, dingnum, cainum, comment_con
            item_loader = SmzdmspiderItemLoader(item=CommentItem(), response=response)
            item_loader.add_value("article_id", article_id)
            item_loader.add_value("article_url", response.url)
            item_loader.add_value("grey", grey)
            item_loader.add_value("usmzdmid", usmzdmid)
            item_loader.add_value("author", author)
            item_loader.add_value("rank", rank)
            item_loader.add_value("comment_time", time)
            item_loader.add_value("comment_con", comment_con)
            item_loader.add_value("come_from", come_from)
            item_loader.add_value("dingnum", dingnum)
            item_loader.add_value("cainum", cainum)

            comment_item = item_loader.load_item()
            yield comment_item


    def parse_member(self, response, follow=True):
        match_obj = re.match(".*?zhiyou.smzdm.com/member/(\d+)/.*?", response.url)
        if match_obj:
            member_id = int(match_obj.group(1))
        item_loader = SmzdmspiderItemLoader(item=MemberItem(), response=response)
        item_loader.add_value("member_id", member_id)
        item_loader.add_css("member_name", '.info-stuff-nickname a::text')
        item_loader.add_css("info_words", '.info-stuff-words::text')
        item_loader.add_css("yuanchuang", '.yuanchuang a::text')
        item_loader.add_css("wiki", '.wiki a::text')
        item_loader.add_css("baoliao", '.baoliao a::text')
        item_loader.add_css("pingce", '.pingce a::text')
        item_loader.add_css("qingdan", '.qingdan a::text')
        item_loader.add_css("comment", '.comment a::text')
        item_loader.add_css("second", '.second a::text')
        item_loader.add_css("focus", '.user-focus span::text')
        item_loader.add_css("fans", '.user-fans span::text')

        member_item = item_loader.load_item()
        yield member_item

