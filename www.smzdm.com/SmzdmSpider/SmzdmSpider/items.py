# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import re
from w3lib.html import remove_tags
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


def get_num(value):
    match_re = re.match(".*?(\d+).*?", value)
    if match_re:
        num = int(match_re.group(1))
    else:
        num = 0
    return num

def remove_blank(value):
    title = ' '.join(value.split())
    return title

def get_grey(value):
    match_re = re.match(".*?(\d+).*?", value)
    if match_re:
        value = int(match_re.group(1))
    elif re.match(u".*?沙发.*?", value):
        value = 1
    elif re.match(u".*?板凳.*?", value):
        value = 2
    elif re.match(u".*?椅子.*?", value):
        value = 3
    else:
        value = 0
    return value


class SmzdmspiderItemLoader(ItemLoader):
    # define the fields for your item here like:
    # name = scrapy.Field()
    default_output_processor = TakeFirst()


class SmzdmArticleItem(scrapy.Item):
    # 构造爆料信息
    article_id = scrapy.Field()
    article_url = scrapy.Field()
    article_title = scrapy.Field(
        input_processor = MapCompose(remove_blank)
    )
    ellipsis_author = scrapy.Field()
    ellipsis_author_id = scrapy.Field()
    update_time = scrapy.Field(
        input_processor = MapCompose(remove_blank)
    )
    price = scrapy.Field()
    buy_url = scrapy.Field()
    price_currency = scrapy.Field()
    price_detail = scrapy.Field()
    content = scrapy.Field()
    fav_num = scrapy.Field(
        input_processor = MapCompose(get_num),
    )
    comment_num = scrapy.Field(
        input_processor = MapCompose(get_num),
    )
    rating_all_num = scrapy.Field(
        input_processor = MapCompose(get_num),
    )
    rating_worthy_num = scrapy.Field(
        input_processor = MapCompose(get_num),
    )
    rating_unworthy_num = scrapy.Field(
        input_processor = MapCompose(get_num),
    )

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO article(article_id, article_url, article_title,
            ellipsis_author, ellipsis_author_id, update_time, price, price_currency, price_detail,
            buy_url, content, fav_num, comment_num,
            rating_all_num, rating_worthy_num, rating_unworthy_num)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE fav_num=VALUES(fav_num), comment_num=VALUES(comment_num), rating_all_num=VALUES(rating_all_num), rating_worthy_num=VALUES(rating_worthy_num), rating_unworthy_num=VALUES(rating_unworthy_num)
        """

        params = (
            self["article_id"], self["article_url"], self["article_title"],
            self["ellipsis_author"], self["ellipsis_author_id"], self['update_time'], self["price"], self["price_currency"], self["price_detail"],
            self["buy_url"], self["content"], self["fav_num"], self["comment_num"],
            self["rating_all_num"], self["rating_worthy_num"], self["rating_unworthy_num"]
        )

        return insert_sql, params


class ArticleTagItem(scrapy.Item):
    # 构造标签
    article_id = scrapy.Field()
    article_url = scrapy.Field()
    tag_sort = scrapy.Field()
    tag_detail = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO article_tag(article_id, article_url, tag_sort, tag_detail)
            VALUES (%s, %s, %s, %s)
        """

        params = (
            self["article_id"], self["article_url"], self["tag_sort"], self["tag_detail"]
        )

        return insert_sql, params


class CommentItem(scrapy.Item):
    # 构造评论
    article_id = scrapy.Field()
    article_url = scrapy.Field()
    grey = scrapy.Field(
        input_processor = MapCompose(get_grey),
    )
    usmzdmid = scrapy.Field()
    author =scrapy.Field()
    rank = scrapy.Field(
        input_processor = MapCompose(get_num),
    )
    comment_con = scrapy.Field()
    dingnum = scrapy.Field(
        input_processor = MapCompose(get_num),
    )
    cainum = scrapy.Field(
        input_processor = MapCompose(get_num),
    )

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO article_comment(article_id, article_url, grey, usmzdmid, author, rank, comment_con, dingnum, cainum)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        params = (
            self["article_id"], self["article_url"], self["grey"], self["usmzdmid"], self["author"], self["rank"],
            self["comment_con"], self["dingnum"], self["cainum"]
        )

        return insert_sql, params
