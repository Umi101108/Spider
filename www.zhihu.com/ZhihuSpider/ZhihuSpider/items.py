# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import datetime
import re

import scrapy
from scrapy.loader.processors import MapCompose

from settings import SQL_DATETIME_FORMAT
from utils.common import extract_num


def get_num(value):
    match_re = re.match(".*?(\d+).*?", value.replace(u',', ''), re.S)
    if match_re:
        num = int(match_re.group(1))
    else:
        num = 0
    return num



class ZhihuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ZhihuQuestionItem(scrapy.Item):
    # 知乎的问题 item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field(
        input_processor = MapCompose(get_num)
    )
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入知乎question表的sql语句
        insert_sql = """
            INSERT INTO zhihu_question(zhihu_id, topics, url, title, content, answer_num, comments_num, watch_user_num, click_num, crawl_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY 
            UPDATE content=VALUES(content), answer_num=VALUES(answer_num), comments_num=VALUES(comments_num), watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
        """
        zhihu_id = self["zhihu_id"][0]
        topics = ",".join(self["topics"])
        url = self["url"][0]
        title = "".join(self["title"])
        content = "".join(self["content"])
        # answer_num = extract_num("".join(self["answer_num"]))
        try:
            answer_num = self["answer_num"][0]
        except:
            answer_num = 0
        # answer_num = self["answer_num"][0] if self["answer_num"][0] else 0
        comments_num = extract_num("".join(self["comments_num"]))

        if len(self["watch_user_num"]) == 2:
            watch_user_num = int(self["watch_user_num"][0])
            click_num = int(self["watch_user_num"][1])
        else:
            watch_user_num = int(self["watch_user_num"][0])
            click_num = 0

        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        params = (zhihu_id, topics, url, title, content, answer_num, comments_num, watch_user_num, click_num, crawl_time)

        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    # 知乎的问题回答item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入知乎question表的sql语句
        insert_sql = """
            INSERT INTO zhihu_answer(zhihu_id, url, question_id, author_id, content, praise_num, comments_num, create_time, update_time, crawl_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            ON DUPLICATE KEY 
            UPDATE content=VALUES(content), comments_num=VALUES(comments_num), praise_num=VALUES(praise_num), update_time=VALUES(update_time)
        """

        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)
        params = (
            self["zhihu_id"], self["url"], self["question_id"],
            self["author_id"], self["content"], self["praise_num"],
            self["comments_num"], create_time, update_time,
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params


class UserItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    avatar_url = scrapy.Field()
    headline = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    url_token = scrapy.Field()
    gender = scrapy.Field()
    cover_url = scrapy.Field()
    type = scrapy.Field()
    badge = scrapy.Field()

    answer_count = scrapy.Field()
    articles_count = scrapy.Field()
    commercial_question_count = scrapy.Field()
    favorite_count = scrapy.Field()
    favorited_count = scrapy.Field()
    follower_count = scrapy.Field()
    following_columns_count = scrapy.Field()
    pins_count = scrapy.Field()
    question_count = scrapy.Field()
    thank_from_count = scrapy.Field()
    thank_to_count = scrapy.Field()
    thanked_count = scrapy.Field()
    vote_from_count = scrapy.Field()
    vote_to_count = scrapy.Field()
    voteup_count = scrapy.Field()
    following_favlists_count = scrapy.Field()
    following_question_count = scrapy.Field()
    following_topic_count = scrapy.Field()
    marked_answers_count = scrapy.Field()
    mutual_followees_count = scrapy.Field()
    hosted_live_count = scrapy.Field()
    participated_live_count = scrapy.Field()

    locations = scrapy.Field()
    educations = scrapy.Field()
    employments = scrapy.Field()




