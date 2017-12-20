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

    # def __init__(self):
    #     COLUMNS = 'productid,standardcd,commonname,tradename,englishname,pinyin,warningsmarks,ingredients,characters,radioactivityandtime,actioncategory,indications,effectsandindications,specification,dosageandadministration,adversereactions,contraindications,warning,cautions,pregnancyandnursingmothers,pediatricuse,geriatricuse,list_interaction,overdosage,clinicaltrails,pharmacologicalandtoxicological,pharmacokinetics,storage,package,usefullife,implementstandard,approvalno,registerno,importlicenceno,corporationname'
    #     for c in COLUMNS:
    #         self[c] = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO bc_product_directiondb_copy(commonname)
                VALUES(%s)
                """
        params = (
            self['commonname'],
        )
        return insert_sql, params
