from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get('http://www.baidu.com')
elem = driver.find_element_by_xpath('')
keyword = ''.encode('utf8')
elem.send_keys(keyword, Keys.RETURN)

html = driver.page_source