# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2017/8/16 上午6:24'

import requests
import time
import MySQLdb

from scrapy.selector import Selector


conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="password", db="xici", charset="utf8")
cursor = conn.cursor()
proxies = {'http':'110.73.49.58:8123'}

def crawl_ips():
    # 爬取西刺的免费ip代理
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
    for i in xrange(10):
        response = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers, proxies=proxies)
        selector = Selector(text=response.text)
        all_trs = selector.css('#ip_list tr')

        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split(u"秒")[0])
            all_texts = tr.css("td::text").extract()

            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[5]

            ip_list.append((ip, port, proxy_type, speed))

        for ip_info in ip_list:
            print ip_info
            # spped = ip_info[3]
            insert_sql = "INSERT INTO proxy_ip(ip, port, proxy_type, speed) VALUES ('{0}', '{1}', '{2}', {3})".format(ip_info[0], ip_info[1], ip_info[2], ip_info[3])
            print insert_sql
            cursor.execute(insert_sql)
            conn.commit()
        time.sleep(3)


class GetIP(object):

    def delete_ip(self, ip):
        # 从数据库中删除无效的ip
        delete_sql = """
            DELETE FROM proxy_ip WHERE ip='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port, proxy_type):
        # 判断ip是否可用
        http_url = "http://www.baidu.com"
        proxy_url = "{0}://{1}:{2}".format(proxy_type, ip, port)
        try:
            proxy_dict = {
                proxy_type: proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict, timeout=3)
        except Exception as e:
            print "invalid ip and port"
            # self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print "effective ip"
                return True
            else:
                print "invalid ip and port"
                # self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从数据库中随机获取一个可用的ip
        random_sql = """
            SELECT ip, port, proxy_type FROM proxy_ip
            ORDER BY RAND()
            LIMIT 1
        """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            proxy_type = ip_info[2]
            print ip_info

            judge_re = self.judge_ip(ip, port, proxy_type)
            if judge_re:
                return "{0}://{1}:{2}".format(proxy_type, ip, port)
            else:
                return self.get_random_ip()

# crawl_ips()
if __name__ == "__main__":
    get_ip = GetIP()
    print get_ip.get_random_ip()
