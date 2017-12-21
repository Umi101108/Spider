# coding: utf-8

def generate(table_name, columns, update_columns='', item_name='SpiderItem'):
    columns_list = columns.split(',')
    result = 'class '+ item_name +'(scrapy.Item):\n'
    for column in columns_list:
        result += '\t' + column + ' = scrapy.Field()\n'
    result += '\n\n\tdef get_insert_sql(self):\n' \
              + '\t\tinsert_sql = """\n\t\t\t\tINSERT INTO ' + table_name \
              + '(' + ', '.join(columns_list) + ')' \
              + '\n\t\t\t\tVALUES(' + ('%s, '*len(columns_list))[:-2] + ')'
    result += '' if update_columns=='' else '\n\t\t\t\tON DUPLICATE KEY UPDATE ' + reduce(lambda a, b: a+', '+b, (map(lambda x: x+'=VALUES('+x+')', update_columns.split(','))))

    result += '\n\t\t\t\t"""\n\t\tparams = (\n\t\t\t'
    for column in columns_list:
        result += 'self["' + column + '"], '
    result += '\n\t\t)\n\t\treturn insert_sql, params'
    print result

if __name__ == '__main__':
    table_name = 'bc_product_directiondb_copy'
    columns = 'commonname,tradename,warningsmarks,ingredients,characters,radioactivityandtime,actioncategory,indications,specification,dosageandadministration,adversereactions,contraindications,warning,cautions,pregnancyandnursingmothers,pediatricuse,geriatricuse,list_interaction,overdosage,clinicaltrails,pharmacologicalandtoxicological,pharmacokinetics,storage,package,usefullife,implementstandard,approvalno,registerno,importlicenceno,corporationname'
    update_columns = ''
    item_name = 'DrugItem'
    generate(table_name, columns, update_columns, item_name)