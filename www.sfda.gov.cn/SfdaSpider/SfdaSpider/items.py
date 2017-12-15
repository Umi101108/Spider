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
    standardcd0 = scrapy.Field()
    standardcdrmk = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO bc_productdb(passno, commonname, englishname, tradename, dosageform, specs, factory, factoryaddr, sort, approvaldate, passnoreg0, standardcd0, standardcdrmk)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        params = (
            self["passno"], self["commonname"], self["englishname"], self["tradename"], self["dosageform"],
            self["specs"], self["factory"], self["factoryaddr"], self["sort"], self["approvaldate"],
            self["passnoreg0"], self["standardcd0"], self["standardcdrmk"]
        )
        return insert_sql, params


class JkypItem(scrapy.Item):
    passno = scrapy.Field()
    passnoreg0 = scrapy.Field()
    packpassnoapp = scrapy.Field()
    firmname = scrapy.Field()
    firmnameen = scrapy.Field()
    firmaddr = scrapy.Field()
    firmaddren = scrapy.Field()
    firmcountry = scrapy.Field()
    firmcountryen = scrapy.Field()
    commonname = scrapy.Field()
    englishname = scrapy.Field()
    tradename = scrapy.Field()
    englishname2 = scrapy.Field()
    dosageform = scrapy.Field()
    specs = scrapy.Field()
    packspecs = scrapy.Field()
    factory = scrapy.Field()
    factoryen = scrapy.Field()
    factoryaddr = scrapy.Field()
    factoryaddren = scrapy.Field()
    factorycountry = scrapy.Field()
    factorycountryen = scrapy.Field()
    approvaldate = scrapy.Field()
    closingdate = scrapy.Field()
    packfirmname = scrapy.Field()
    packfirmaddr = scrapy.Field()
    category = scrapy.Field()
    standardcd0 = scrapy.Field()
    standardcdrmk = scrapy.Field()
    importflg = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO bc_productdb2(passno, passnoreg0, packpassnoapp, firmname, firmnameen, \
                firmaddr, firmaddren, firmcountry, firmcountryen, commonname, \
                englishname, tradename, englishname2, dosageform, specs, \
                packspecs, factory, factoryen, factoryaddr, factoryaddren, \
                factorycountry, factorycountryen, approvaldate, closingdate, packfirmname, \
                packfirmaddr, category, standardcd0, standardcdrmk, importflg)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        self["importflg"] = '1'
        params = (
            self["passno"], self["passnoreg0"], self["packpassnoapp"], self["firmname"], self["firmnameen"],
            self["firmaddr"], self["firmaddren"], self["firmcountry"], self["firmcountryen"], self["commonname"],
            self["englishname"], self["tradename"], self["englishname2"], self["dosageform"], self["specs"],
            self["packspecs"], self["factory"], self["factoryen"], self["factoryaddr"], self["factoryaddren"],
            self["factorycountry"], self["factorycountryen"], self["approvaldate"], self["closingdate"], self["packfirmname"],
            self["packfirmaddr"], self["category"], self["standardcd0"], self["standardcdrmk"], self["importflg"],
        )
        return insert_sql, params