# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

def strip(path):
    path = re.sub(r'[?\\*|"<>:/]', '', str(path))
    return path

class MzituspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        folder = item['title']
        folder_strip = strip(folder)
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(folder_strip, image_guid)
        return filename

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            referer = item['url']
            yield scrapy.Request(image_url, meta={'item': item, 'referer': referer})

    def item_completed(self, results, item, info):
        image_paths = [value['path'] for ok, value in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item["image_path"] = image_paths
        return item