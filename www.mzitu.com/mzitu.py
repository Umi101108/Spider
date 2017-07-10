# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os


class Mzitu(object):

    def __init__(self):
        self.pwd = "/Users/umi/Pictures/meizitu/"
        self.root_url = 'http://www.mzitu.com/all/'
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

    def getList(self, soup):
        allyears = soup.select('div.all')[0]
        archives = allyears.select('a')
        for archive in archives:
            title = archive.get_text().strip().replace('?', '_')
            imgs_url = archive.get('href')
            self.mkdir(title)
            os.chdir(self.pwd+title)
            print u"开始下载：" + title
            self.getImgs(imgs_url)

    def getImgs(self, url):
        imgs_soup = self.getSoup(url)
        if imgs_soup:
            max_pageno = imgs_soup.select('div.pagenavi')[0].select('span')[-2].get_text()
            for pageno in xrange(1, int(max_pageno)+1):
                img_page = url + '/' + str(pageno)
                img_soup = self.getSoup(img_page)
                img_url = img_soup.select('div.main-image > p > a > img')[0].get('src')
                self.saveImg(img_url)
            print u"成功下载" + max_pageno + u"张图片"

    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(os.path.join(self.pwd, path))
        if not isExists:
            print u"新建了一个名为" + path + u"的文件夹"
            os.makedirs(os.path.join(self.pwd, path))
        else:
            print u"名字叫做" + path + u"的文件夹已经存在了！"
            return True

    def saveImg(self, url):
        name = url.split('/')[-1]
        img = requests.get(url, headers=self.headers).content
        with open(name, 'wb') as filename:
            filename.write(img)

    def main(self):
        soup = self.getSoup(self.root_url)
        self.getList(soup)

if __name__ == "__main__":
    mzitu = Mzitu()
    mzitu.main()
