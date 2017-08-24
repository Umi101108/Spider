# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SmzdmspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SmzdmPostItem(scrapy.Item):
    # 构造爆料信息
    article_url = scrapy.Field()
    article_title = scrapy.Field()
    ellipsis_author = scrapy.Field()
    ellipsis_author_id = scrapy.Field()
    update_time = scrapy.Field()
    price = scrapy.Field()
    price_currency = scrapy.Field()
    content = scrapy.Field()
    fav_num = scrapy.Field()
    comment_num = scrapy.Field()
    tags = scrapy.Field()
    rating_all_num = scrapy.Field()
    rating_worthy_num = scrapy.Field()
    rating_unworthy_num = scrapy.Field()


class PostTagItem(scrapy.Item):
    # 构造标签
    article_url = scrapy.Field()
    tag_sort = scrapy.Field()
    tag_detail = scrapy.Field()


class CommentItem(scrapy.Item):
    # 构造评论
    grey = scrapy.Field()
    usmzdmid = scrapy.Field()
    author =scrapy.Field()
    rank = scrapy.Field()
    comment_con = scrapy.Field()
    dingnum = scrapy.Field()
    cainum = scrapy.Field()

