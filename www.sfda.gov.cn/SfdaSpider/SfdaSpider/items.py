# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SfdaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GcypItem(scrapy.Item):
    passno = scrapy.Field()
    commonname = scrapy.Field()
    englishname = scrapy.Field()
    tradename = scrapy.Field()
    dosageform = scrapy.Field()
    specs = scrapy.Field()
    factory = scrapy.Field()
    factoryaddr = scrapy.Field()
    sort = scrapy.Field()
    approvaldate = scrapy.Field()
    passnoreg0 = scrapy.Field()
    standardcd = scrapy.Field()
    standardcdrmk = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO bc_productdb(passno, commonname, englishname, tradename, dosageform, specs, factory, factoryaddr, sort, approvaldate, passnoreg0, standardcd, standardcdrmk)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        params = (
            self["passno"], self["commonname"], self["englishname"], self["tradename"], self["dosageform"],
            self["specs"], self["factory"], self["factoryaddr"], self["sort"], self["approvaldate"],
            self["passnoreg0"], self["standardcd"], self["standardcdrmk"]
        )
        return insert_sql, params