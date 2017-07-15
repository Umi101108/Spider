# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import random
import re
import time


class Xicidaili(object):

    def __init__(self):
        self.base_url = "http://www.xicidaili.com/nn/"
        self.test_url = "http://www.cnblogs.com/juandx/p/5620126.html"
        self.set_timeout = 2
        self.IP_list = {}
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        self.headers = {'User-Agent': self.user_agent}

    def getSoup(self, url, proxies=None, timeout=3):
        response = requests.get(url, headers=self.headers, proxies=proxies)
        if response.status_code == 200:
            html = response.content
            soup = BeautifulSoup(html, 'lxml')
            return soup
        else:
            print "该网页不存在"
            return

    def isAlive(self, ip_type, ip, port):
        proxy = {ip_type.lower():ip+':'+port}
        try:
            response = requests.get(self.test_url, headers=self.headers, proxies=proxy, timeout=3)
            if response.status_code == 200:
                print proxy, "可用"
                self.IP_list[ip+':'+port] = ip_type.lower()
            else:
                print "不可用"
        except:
            print proxy, "不可用"
            pass

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
        for k, v in self.IP_list.iteritems():
            print k, v
        
        for i in xrange(10000):
            proxies = self.getRandomProxy()
            try:
                response = requests.get('https://www.douban.com/group/shanghaizufang/', headers=self.headers, proxies=proxies, timeout=0.5)
                print response
            except:
                pass


if __name__ == '__main__':
    xicidaili = Xicidaili()
    xicidaili.main()