# -*- coding: utf-8 -*-

from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time

# driver = webdriver.Chrome("/Users/umi/Downloads/chromedriver")
driver = webdriver.PhantomJS("/Users/umi/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs")
# driver.get('http://music.163.com/m/user/home?id=371821058')
# driver.switch_to_frame('g_iframe')
# elem_songsall = driver.find_element_by_xpath('//*[@id="songsall"]')
# elem_songsall.click()
# elem_more = driver.find_element_by_xpath('//div[@class="more"]')
# elem_more.click()
# print driver.page_source
songs_url = "http://music.163.com/user/songs/rank?id=371821058"
# driver = webdriver.Chrome("/Users/umi/Downloads/chromedriver")
driver.get(songs_url)
driver.switch_to_frame('g_iframe')
# wait = ui.WebDriverWait(driver, 15)
# wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="songsall"]'))
# elem_songsall = driver.find_element_by_xpath('//*[@id="songsall"]')
# elem_songsall.click()

songs_record = driver.find_element_by_xpath('//div[@id="m-record"]')
# print driver.page_source
# print song
time.sleep(2)
songs = songs_record.find_elements_by_xpath('//li')
print driver.page_source
for song in songs:
    print song.text

