# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2017/8/16 下午10:47'

from selenium import webdriver

driver = webdriver.PhantomJS(executable_path="/Users/umi/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs")

driver.get("https://detail.tmall.com/item.htm?spm=a1z0d.6639537.1997196601.16.91b1f81392iq7&id=544470704201&sku_properties=5919063:6536025")
print driver.page_source879