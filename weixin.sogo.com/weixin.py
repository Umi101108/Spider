# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2018/4/24 下午5:16'

import requests
from requests.exceptions import ConnectionError
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import pymongo

client = pymongo.MongoClient('localhost')
db = client['weixin']


base_url = 'http://weixin.sogou.com/weixin?'

keyword = '海贼王'
proxy_pool_url = 'http://127.0.0.1:5000/get'
proxy = None
max_count = 5

headers = {
    'Host': 'weixin.sogou.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15'
}

def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def get_html(url, count=1):
    global proxy
    print ("Crawling", url)
    print ("Trying Count", count)
    if count >= max_count:
        print ("Tried Too Many Counts")
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)

        if response.status_code == 200:
            return response.text
        elif response.status_code == 302:
            print ("302")
            proxy = get_proxy()
            if proxy:
                print ("Using Proxy", proxy)
                return get_html()
            else:
                print ("Get Proxy Failed")
                return None
            pass
    except ConnectionError as e:
        print ("Error Occured", e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)

def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html

def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')

def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def parse_detail(html):
    try:
        doc = pq(html)
        title = doc('.rich_media_title').text()
        content = doc('.rich_media_content').text()
        date = doc('#post-date').text()
        nickname = doc('#post-user').text()
        wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        return {
            'title': title,
            'content': content,
            'date': date,
            'nickname': nickname,
            'wechat': wechat
        }
    except:
        return None

def save_to_mongo(data):
    if db['articles'].update({'title': data['title']}, {'$set': data}, True):
        print ('Saved to Mongo', data['title'])
    else:
        print ('Saved to Mongo Failed', data['title'])


def main():
    for page in range(1, 2):
        html = get_index(keyword, page)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html =  get_detail(article_url)
                if article_html:
                    article_data = parse_detail(article_html)
                    print (article_data)
                    if article_data:
                        save_to_mongo(article_data)


if __name__ == '__main__':
    main()