# -*- coding: utf-8 -*-

from selenium import webdriver

# driver = webdriver.Chrome("/Users/umi/Downloads/chromedriver")
driver = webdriver.PhantomJS("/Users/umi/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs")
driver.get('https://www.baidu.com')
news = driver.find_element_by_xpath("//div[@id='u1']/a")
print news.text
