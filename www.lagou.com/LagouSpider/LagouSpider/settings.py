# -*- coding: utf-8 -*-

# Scrapy settings for LagouSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os
import sys

BOT_NAME = 'LagouSpider'

SPIDER_MODULES = ['LagouSpider.spiders']
NEWSPIDER_MODULE = 'LagouSpider.spiders'

project_dir = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

sys.path.insert(0, os.path.join(BASE_DIR, 'LagouSpider'))

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'LagouSpider (+http://www.yourdomain.com)'
RANDOM_UA_TYPE = "random"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Cookie': 'user_trace_token=20170814195322-05a936db-0205-4ffc-92ac-834581d556da; LGUID=20170814195325-2dcd65e5-80e7-11e7-8763-5254005c3644; index_location_city=%E4%B8%8A%E6%B5%B7; JSESSIONID=ABAAABAACBHABBI334F08E054E02D8367D4CBC215204BA5; TG-TRACK-CODE=index_hotjob; X_HTTP_TOKEN=7a0514a870dea9356bebb13166332ee4; _gat=1; _ga=GA1.2.1603059751.1502711624; _gid=GA1.2.1863629284.1503586875; LGSID=20170824230109-101291ae-88dd-11e7-a740-525400f775ce; LGRID=20170824233457-c88cf105-88e1-11e7-8ea0-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1502711624,1503586875; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1503588903',
    'Referer': 'https://www.lagou.com'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'LagouSpider.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'LagouSpider.middlewares.MyCustomDownloaderMiddleware': 543,
    'LagouSpider.middlewares.RandomUserAgentMiddleware': 1,
    'LagouSpider.middlewares.RandomProxyMiddleware': 2,
   #  'LagouSpider.middlewares.JSPageMiddleware': 1,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'LagouSpider.pipelines.MysqlTwistedPipline': 1,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MYSQL_HOST = "127.0.0.1"
MYSQL_DBNAME = "lagou"
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"


SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"