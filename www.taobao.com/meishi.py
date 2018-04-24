# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2018/4/24 下午2:58'

import re
from pyquery import PyQuery as pq
import pymongo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from config import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

options = Options()
options.add_argument('-headless')
browser = webdriver.Chrome("/Users/umi/Downloads/chromedriver", chrome_options=options)
# browser = webdriver.PhantomJS("/Users/umi/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs")
wait = WebDriverWait(browser, 10)

browser.set_window_size(1400, 900)


def search():
    print ("正在搜索")
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
        )
        input.send_keys(KEYWORD)
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
        )
        get_products()
        return total.text
    except:
        return search()

def next_page(page_number):
    print ("正在翻页", page_number)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span '), str(page_number))
        )
        get_products()
    except:
        next_page(page_number)

def get_products():
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item'))
    )
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text()[2: ],
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print (product)
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print ('存储到MongoDB成功', result)
    except Exception:
        print ('存储到MongoDB失败', result)


def main():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))
        print (total)
        for i in range(2, total+1):
            next_page(i)
    except Exception:
        print ("出错啦")
    finally:
        browser.close()


if __name__ == '__main__':
    main()