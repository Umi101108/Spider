# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2017/8/16 下午10:47'

import time
from selenium import webdriver
from scrapy.selector import Selector


# driver = webdriver.PhantomJS(executable_path="/Users/umi/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs")
driver = webdriver.Chrome("/Users/umi/Downloads/chromedriver")

# driver.get("https://detail.tmall.com/item.htm?spm=a1z0d.6639537.1997196601.16.91b1f81392iq7&id=544470704201&sku_properties=5919063:6536025")
# t_selector = Selector(text=driver.page_source)
# print t_selector.css(".tm-price::text").extract()
# driver.quit()

# account = "13175810927"
# password = "5PN-Dsu-BMg-RLf"
# driver.get("https://www.zhihu.com/#signin")
# driver.find_element_by_css_selector(".signin-switch-password").click()
# driver.find_element_by_css_selector(".view-signin input[name='account']").send_keys(account)
# driver.find_element_by_css_selector(".view-signin input[name='password']").send_keys(password)
# driver.find_element_by_css_selector("button.sign-button").click()
# print driver.page_source
# driver.quit()


chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chrome_opt.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome("/Users/umi/Downloads/chromedriver", chrome_options=chrome_opt)

driver.get("https://www.oschina.net/blog")
script_scrolldown = """
    window.scrollTo(0, document.body.scrollHeight);
    var lenOfPage=document.body.scrollHeight;
    return lenOfPage;
"""
for i in xrange(3):
    driver.execute_script(script_scrolldown)
    time.sleep(3)
