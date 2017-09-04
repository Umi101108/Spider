# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import re
import datetime
from w3lib.html import remove_tags
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst

from settings import SQL_DATE_FORMAT, SQL_DATETIME_FORMAT


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

def get_publish_time(value):
    match_re_ymd = re.match(u".*?(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", value)
    match_re_md = re.match(u".*?(\d{2}-\d{2} \d{2}:\d{2})", value)
    match_re_h = re.match(u".*?(\d{2}:\d{2})", value)
    if match_re_ymd:
        # publish_time = datetime.datetime.strptime(match_re_ymd.group(1), '%Y-%m-%d %H:%M')
        publish_time = match_re_ymd.group(1)
    elif match_re_md:
        # publish_time = datetime.datetime.strptime(match_re_md.group(1), '%m-%d %H:%M')
        publish_time = str(datetime.datetime.now().year) + "-"+ match_re_md.group(1)
    elif match_re_h:
        # publish_time = datetime.datetime.strptime(match_re_h.group(1), '%H:%M')
        publish_time = str(datetime.datetime.now().strftime('%Y-%m-%d')) + " " + match_re_h.group(1)
    else:
        publish_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
    return publish_time

def get_comment_time(value):
    if re.match(u".*?分钟.*?", value):
        minutes = int(re.sub('\D', '', value))
        current_time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
        comment_time = current_time.strftime(SQL_DATETIME_FORMAT)
    elif re.match(u".*?小时.*?", value):
        minutes = int(re.sub('\D', '', value))*60
        current_time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
        comment_time = current_time.strftime(SQL_DATETIME_FORMAT)
    elif re.match(u".*?刚刚.*?", value):
        minutes = 0
        current_time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
        comment_time = current_time.strftime(SQL_DATETIME_FORMAT)
    # print comment_time
    else:
        comment_time = get_publish_time(value)
    # current_time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
    # comment_time = current_time.strftime(SQL_DATETIME_FORMAT)
    return comment_time







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
        input_processor = MapCompose(get_publish_time)
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
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO article(article_id, article_url, article_title,
            ellipsis_author, ellipsis_author_id, update_time, price, price_currency, price_detail,
            buy_url, content, fav_num, comment_num,
            rating_all_num, rating_worthy_num, rating_unworthy_num, crawl_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE fav_num=VALUES(fav_num), comment_num=VALUES(comment_num), rating_all_num=VALUES(rating_all_num), rating_worthy_num=VALUES(rating_worthy_num), rating_unworthy_num=VALUES(rating_unworthy_num)
        """
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        params = (
            self["article_id"], self["article_url"], self["article_title"],
            self["ellipsis_author"], self["ellipsis_author_id"], self['update_time'], self["price"], self["price_currency"], self["price_detail"],
            self["buy_url"], self["content"], self["fav_num"], self["comment_num"],
            self["rating_all_num"], self["rating_worthy_num"], self["rating_unworthy_num"],
            crawl_time
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
    comment_time = scrapy.Field(
        input_processor = MapCompose(get_comment_time)
    )
    come_from = scrapy.Field()
    dingnum = scrapy.Field(
        input_processor = MapCompose(get_num),
    )
    cainum = scrapy.Field(
        input_processor = MapCompose(get_num),
    )

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO article_comment(article_id, article_url, grey, usmzdmid, author, rank, comment_con, comment_time, come_from, dingnum, cainum, crawl_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE dingnum=VALUES(dingnum), cainum=VALUES(cainum)
        """
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        params = (
            self["article_id"], self["article_url"], self["grey"], self["usmzdmid"], self["author"], self["rank"],
            self["comment_con"], self["comment_time"], self["come_from"], self["dingnum"], self["cainum"], crawl_time
        )

        return insert_sql, params


class MemberItem(scrapy.Item):
    # 构造用户信息
    member_id = scrapy.Field()
    member_name = scrapy.Field()
    info_words = scrapy.Field(
        input_processor = MapCompose(remove_blank),
    )
    yuanchuang = scrapy.Field(
        input_processor=MapCompose(get_num),
    )
    wiki = scrapy.Field(
        input_processor = MapCompose(get_num),
    )
    baoliao = scrapy.Field(
        input_processor=MapCompose(get_num),
    )
    pingce = scrapy.Field(
        input_processor=MapCompose(get_num),
    )
    qingdan = scrapy.Field(
        input_processor=MapCompose(get_num),
    )
    comment = scrapy.Field(
        input_processor=MapCompose(get_num),
    )
    second = scrapy.Field(
        input_processor=MapCompose(get_num),
    )
    focus = scrapy.Field(
        input_processor=MapCompose(get_num),
    )
    fans = scrapy.Field(
        input_processor=MapCompose(get_num),
    )

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO member(member_id, member_name, info_words, focus, fans, yuanchuang, wiki, baoliao, pingce, qingdan, comment, `second`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE focus=VALUES(focus), fans=VALUES(fans), yuanchuang=VALUES(yuanchuang), wiki=VALUES(wiki), baoliao=VALUES(baoliao), pingce=VALUES(pingce), comment=VALUES(comment), `second`=VALUES(`second`)
        """

        params = (
            self["member_id"], self["member_name"], self["info_words"], self["focus"], self["fans"],
            self["yuanchuang"], self["wiki"], self["baoliao"], self["pingce"], self["qingdan"], self["comment"], self["second"]
        )
        return insert_sql, params