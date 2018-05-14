# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeibospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name = 'weibo'

    id = scrapy.Field()
    content = scrapy.Field()
    forward_count = scrapy.Field()
    comment_count = scrapy.Field()
    like_count = scrapy.Field()
    posted_at = scrapy.Field()
    url = scrapy.Field()
    user = scrapy.Field()
    # crawled_at = scrapy.Field()
