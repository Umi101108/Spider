# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import time
import datetime
import pymongo
from items import WeibospiderItem


class WeibospiderPipeline(object):
    def parse_time(self, posted_at):
        posted_at = posted_at.strip()
        if re.match('\d+月\d+日', posted_at):
            match = re.match('(\d+)月(\d+)日(.*)', posted_at)
            posted_at = str(datetime.datetime.now().year) + '-' + match.group(1) + '-' + match.group(2) + match.group(3)
        elif re.match('\d+分钟前', posted_at):
            match = re.match('(\d+)分钟前', posted_at)
            minutes = int(match.group(1))
            posted_at = (datetime.datetime.now() - datetime.timedelta(minutes=minutes)).strftime('%Y-%m-%d %H:%M')
        elif re.match('今天.*', posted_at):
            match = re.match('今天(.*)', posted_at)
            posted_at = str(datetime.datetime.now().strftime('%Y-%m-%d')) + match.group(1)
        # if re.match('\d+月\d+日', posted_at):
        #     posted_at = time.strftime('%Y年', time.localtime()) + posted_at
        # elif re.match('\d+分钟前', posted_at):
        #     test = time.strftime('%Y年', time.localtime())
        #     minute = re.match('(\d+)', posted_at).group(1)
        #     posted_at = time.strftime('%Y年%m月%d日 %H:%M', time.localtime(time.time()-float(minute)*60))
        # elif re.match('今天.*', posted_at):
        #     test = time.strftime('%Y年', time.localtime())
        #     datetime = re.match('今天(.*)', posted_at).group(1).strip()
        #     posted_at = time.strftime('%Y年%m月%d日', time.localtime()) + ' ' + posted_at
        return posted_at

    def process_item(self, item, spider):
        print (item)
        if isinstance(item, WeibospiderItem):
            if item.get('content'):
                item['content'] = item['content'].lstrip(':').strip()
            if item.get('posted_at'):
                item['posted_at'] = self.parse_time(item['posted_at'])
        print (item)
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[item.table_name].update({'id': item.get('id')}, {'$set': dict(item)}, True)
        return item