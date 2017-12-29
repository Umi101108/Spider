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
    productid = scrapy.Field()
    commonname = scrapy.Field()
    tradename = scrapy.Field()
    warningsmarks = scrapy.Field()
    ingredients = scrapy.Field()
    characters = scrapy.Field()
    radioactivityandtime = scrapy.Field()
    actioncategory = scrapy.Field()
    indications = scrapy.Field()
    specification = scrapy.Field()
    dosageandadministration = scrapy.Field()
    adversereactions = scrapy.Field()
    contraindications = scrapy.Field()
    warning = scrapy.Field()
    cautions = scrapy.Field()
    pregnancyandnursingmothers = scrapy.Field()
    pediatricuse = scrapy.Field()
    geriatricuse = scrapy.Field()
    list_interaction = scrapy.Field()
    overdosage = scrapy.Field()
    clinicaltrails = scrapy.Field()
    pharmacologicalandtoxicological = scrapy.Field()
    pharmacokinetics = scrapy.Field()
    storage = scrapy.Field()
    package = scrapy.Field()
    usefullife = scrapy.Field()
    implementstandard = scrapy.Field()
    approvalno = scrapy.Field()
    registerno = scrapy.Field()
    importlicenceno = scrapy.Field()
    corporationname = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
				INSERT INTO 4_bc_product_directiondb_copy(productid, commonname, tradename, warningsmarks, ingredients, characters, radioactivityandtime, actioncategory, indications, specification, dosageandadministration, adversereactions, contraindications, warning, cautions, pregnancyandnursingmothers, pediatricuse, geriatricuse, list_interaction, overdosage, clinicaltrails, pharmacologicalandtoxicological, pharmacokinetics, storage, package, usefullife, implementstandard, approvalno, registerno, importlicenceno, corporationname)
				VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
				"""
        params = (
            self["productid"], self["commonname"], self["tradename"], self["warningsmarks"], self["ingredients"],
            self["characters"], self["radioactivityandtime"], self["actioncategory"], self["indications"],
            self["specification"], self["dosageandadministration"], self["adversereactions"], self["contraindications"],
            self["warning"], self["cautions"], self["pregnancyandnursingmothers"], self["pediatricuse"],
            self["geriatricuse"], self["list_interaction"], self["overdosage"], self["clinicaltrails"],
            self["pharmacologicalandtoxicological"], self["pharmacokinetics"], self["storage"], self["package"],
            self["usefullife"], self["implementstandard"], self["approvalno"], self["registerno"],
            self["importlicenceno"], self["corporationname"],
        )
        return insert_sql, params
