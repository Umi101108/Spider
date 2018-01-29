# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2018/1/29 下午11:33'
"""
弹幕中p属性含义
9.03300,1,25,16777215,1517118568,0,41295bb0,4221201695
1.弹幕出现的时间（单位：秒）
2.弹幕模式：1-3 滚动弹幕、4 底端弹幕、5 顶端弹幕、6 逆向弹幕、7 精准定位、8 高级弹幕
3.字号： 12 非常小、16 特小、18 小、25 中、36 大、45 很大、64 特别大
4.字体颜色（以HTML颜色的十进制为准）
5.Unix格式的时间戳
6.弹幕池：0 普通池、1 字幕池、2 特殊池（高级弹幕专用）
7.发送者ID，用于“屏蔽此弹幕的发送者”
8.弹幕数据库中rowID，用于“历史弹幕”功能
"""

from datetime import datetime
import re
import MySQLdb
import requests
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf8')



class Bilibili(object):
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
        self.headers = {'User-Agent': self.user_agent}
        try:
            self.conn = MySQLdb.connect(
                host='localhost',
                port=3307,
                user='root',
                passwd='123456',
                db='bilibili'
            )
            self.cur = self.conn.cursor()
        except MySQLdb.Error, e:
            print "数据库连接错误，原因为%d: %s" % (e.args[0], e.args[1])

    def insertData(self, table, my_dict):
        try:
            self.conn.set_character_set('utf8')
            cols = ', '.join(my_dict.keys())
            values = '", "'.join(my_dict.values())
            sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, '"' + values + '"')
            print sql
            try:
                result = self.cur.execute(sql)
                insert_id = self.conn.insert_id()
                self.conn.commit()
                if result:
                    return insert_id
                else:
                    return 0
            except MySQLdb.Error, e:
                self.conn.rollback()
                if "key 'PRIMARY'" in e.args[1]:
                    print "数据已存在，未插入数据"
                else:
                    print "数据插入失败，原因 %d: %s" % (e.args[0], e.args[1])
        except MySQLdb.Error, e:
            print "数据库错误，原因 %d: %s" % (e.args[0], e.args[1])

    def get_bullet(self, aid, cid):
        table = 'bullet'
        url = 'http://comment.bilibili.com/{cid}.xml'.format(cid=cid)
        response = requests.get(url=url, headers=self.headers)
        html = response.content
        soup = BeautifulSoup(html, 'lxml')
        infos = soup.select('d')
        for info in infos:
            data = info.get('p').split(',')
            content = {
                'aid': str(aid),
                'cid': str(cid),
                'show_time': data[0],
                'content': info.get_text(),
                'type': data[1],
                'font_size': data[2],
                'color': data[3],
                'timestamp': data[4],
                'pool': data[5],
                'sender_id': data[6],
                'row_id': data[7]
            }
            self.insertData(table, content)
            print datetime.fromtimestamp(float(info.get('p').split(',')[4])), info.get_text()

    def get_cid(self, av_id):
        url = 'https://www.bilibili.com/video/av{av_id}'.format(av_id=av_id)
        response = requests.get(url=url, headers=self.headers)
        html = response.content
        return re.match(r'.*?cid=(.*?)&', html, re.S).group(1)

    def get_videos(self, userid):
        table = 'video'
        av_list = []
        url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid={userid}&pagesize=30&tid=0&page={pageno}&keyword=&order=pubdate'.format(
            pageno=1, userid=userid)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
        response = requests.get(url=url, headers=headers)
        html = response.json()
        pages = html['data']['pages']
        for page in xrange(1, int(pages) + 1):
            url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid={userid}&pagesize=30&tid=0&page={pageno}&keyword=&order=pubdate'.format(
                pageno=page, userid=userid)
            print url
            response = requests.get(url=url, headers=headers)
            html = response.json()
            video_list = html['data']['vlist']
            for video in video_list:
                av_list.append(video)
                content = {
                    'aid': video['aid'],
                    'author': video['author'],
                    'comment': video['comment'],
                    'copyright': video['copyright'],
                    'created': video['created'],
                    'description': video['description'],
                    'favorites': video['favorites'],
                    'hide_click': video['hide_click'],
                    'length': video['length'],
                    'mid': video['mid'],
                    'pic': video['pic'],
                    'play': video['play'],
                    'review': video['review'],
                    'subtitle': video['subtitle'],
                    'title': video['title'],
                    'typeid': video['typeid'],
                    'video_review': video['video_review']
                }
                for k, v in content.iteritems():
                    if type(v) == int:
                        content[k] = str(v)
                self.insertData(table, {k: str(v) for k, v in content.iteritems()})
        return av_list

    def main(self):
        userid = '7737474'
        userid = '27669924'
        videos = self.get_videos(userid)
        for video in videos:
            print video['aid'], video['title'], datetime.fromtimestamp(video['created']), '播放', video['play'], '收藏', \
            video['favorites'], '评论', video['comment']
            self.get_bullet(video['aid'], self.get_cid(video['aid']))


if __name__ == '__main__':
    Bilibili().main()

