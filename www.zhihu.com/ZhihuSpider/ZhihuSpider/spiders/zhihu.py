# -*- coding: utf-8 -*-

import re
import json
import time
from urlparse import urljoin
from PIL import Image
import scrapy


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = (
        'http://www.zhihu.com/',
    )

    # question的第一页answer的请求url
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    }

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.headers, callback=self.login)]

    def login(self, response):
        response_text = response.text
        # 获取xsrf
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response_text, re.DOTALL)
        xsrf = ''
        if match_obj:
            xsrf = match_obj.group(1)

        if xsrf:
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": xsrf,
                "phone_num": "phone",
                "password": "password",
            }
            t = str(int(time.time())*1000)
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
            # 请求验证码并回调login_after_captcha
            yield scrapy.Request(captcha_url, headers=self.headers, meta={"post_data": post_data}, callback=self.login_after_captcha)

    def login_after_captcha(self, response):
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()

        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass

        captcha = input("请输入验证码\n>")

        post_data = response.meta.get("post_data", {})
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data['captcha'] = captcha
        return [scrapy.FormRequest(url=post_url, formdata=post_data, headers=self.headers, callback=self.check_login)]

    def check_login(self, response):
        # 验证服务器的返回数据判断是否成功
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == u"登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)


    def parse(self, response):
        """
        提取出html页面的所有url，并跟踪这些url进行一步爬取
        如果提取的url中格式为 /question/xxx 就下载之后进入解析函数
        :param response: 
        :return: 
        """
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [urljoin(response.url, url) for url in all_urls]
        # 使用lambda函数对每一个url进行过滤，如果是true放回列表，如果是false则去除
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*?", url)
            if match_obj:
                # 如果提取到question相关的页面则下载后交由提取函数进行提取
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
            else:
                # 如果不是question页面则直接进一步跟踪
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)



