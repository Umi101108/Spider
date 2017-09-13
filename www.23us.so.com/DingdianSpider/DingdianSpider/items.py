# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import datetime

import scrapy
from settings import SQL_DATE_FORMAT, SQL_DATETIME_FORMAT

class DingdianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    novel_url = scrapy.Field()
    serial_status = scrapy.Field()
    serial_num = scrapy.Field()
    category = scrapy.Field()
    id = scrapy.Field()
    click_num = scrapy.Field()
    fav_num = scrapy.Field()


    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO novel(id, name, author, novel_url, category, serial_num, serial_status, click_num, fav_num)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        params = (
            self["id"], self["name"], self["author"], self["novel_url"],
            self["category"], self["serial_num"], self["serial_status"],
            self["click_num"], self["fav_num"]
        )

        return insert_sql, params


class DingdianContentItem(scrapy.Item):
    novel_id = scrapy.Field()
    novel_name = scrapy.Field()
    chapter_name = scrapy.Field()
    chapter_no = scrapy.Field()
    content = scrapy.Field()
    chapter_url = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO novel_content(novel_id, novel_name, chapter_name, chapter_no, content, chapter_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            self["novel_id"], self["novel_name"], self["chapter_name"], self["chapter_no"], self["content"], self["chapter_url"]
        )

        return insert_sql, params