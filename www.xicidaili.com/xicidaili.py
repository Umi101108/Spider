# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import random
import re
import time


class Xicidaili(object):

    def __init__(self):
        self.base_url = "http://www.xicidaili.com/nn/"
        self.test_url = "http://www.maishoudang.com/deals/ya-ma-xun-primeday-jia-dian-zhuan-chang-hao-jia-he-ji-98598"
        self.set_timeout = 2
        self.IP_list = {}
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        self.headers = {'User-Agent': self.user_agent}

    def getSoup(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            html = response.content
            soup = BeautifulSoup(html, 'lxml')
            return soup
        else:
            print "该网页不存在"
            return

    def isAlive(self, ip_type, ip, port, set_timeout=3):
        # ip = '11111.11111.111.111'
        proxy = {ip_type:ip+':'+port}
        response = requests.get(self.test_url, headers=self.headers, proxies=proxy, timeout=self.set_timeout)
        if response.status_code == 200:
            # print proxy, "可用"
            self.IP_list[ip+':'+port] = ip_type
        else:
            print "不可用"

    def getRandomProxy(self):
        ip = random.choice(self.IP_list.keys())
        ip_type = self.IP_list[ip]
        return {ip_type:ip}

    def main(self):
        soup = self.getSoup(self.base_url)
        ip_list = soup.select('table#ip_list')[0].select('tr')[1:]
        for ip_info in ip_list:
            ip = ip_info.select('td')[1].get_text()
            port = ip_info.select('td')[2].get_text()
            ip_type = ip_info.select('td')[5].get_text()
            self.isAlive(ip_type, ip, port)
        # for k, v in self.IP_list.iteritems():
        #     print k, v
        print self.getRandomProxy()






if __name__ == '__main__':
    xicidaili = Xicidaili()
    xicidaili.main()
