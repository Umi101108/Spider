# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JiankespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DrugItem(scrapy.Item):
    commonname
    tradename
    ingredients
    characters
    indications
    specification
    dosageandadministration
    adversereactions
    contraindications
    cautions
    list_interaction
    storage
    package
    usefullife
    implementstandard
    approvalno
    corporationname