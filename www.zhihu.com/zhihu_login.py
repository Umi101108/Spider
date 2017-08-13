# -*- coding: utf-8 -*-

import requests
import re
import cookielib

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
try:
    session.cookies.load(ignore_discard=True)
except:
    print "cookie未能加载"

user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36"
headers = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": user_agent,
}

def is_login():
    # 通过个人中心页面返回状态码来判断是否为登录状态
    inbox_url = "https://www.zhihu.com/question/56250357/answer/148534773"
    response = session.get(inbox_url, headers=headers, allow_redirects=True)
    # print response.text
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    if response.status_code != 200:
        return False
    else:
        return True

def get_xsrf():
    # 获取xsrf code
    response = session.get("http://www.zhihu.com", headers=headers)
    html = response.text
    # reDOTALL匹配全文
    match_obj = re.match('.*?name="_xsrf" value="(.*?)"', html, re.DOTALL)
    xsrf = match_obj.group(1) if match_obj else ''
    return xsrf

def get_index():
    response = session.get("https://www.zhihu.com", headers=headers)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print "ok"

def get_captcha():
    import time
    t = str(int(time.time()*1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
    t = session.get(captcha_url, headers=headers)
    with open("captcha.jpg", "wb") as f:
        f.write(t.content)
        f.close()

    from PIL import Image
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        pass

    captcha = raw_input("输入验证码\n>")
    return captcha

def zhihu_login(account, password):
    # 知乎登录
    if re.match("^1\d{10}", account):
        print "手机号登录"
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password,
            "captcha": get_captcha()
        }
    elif "@" in account:
        # 判断用户名是否为邮箱
        print("邮箱方式登录")
        post_url = "https://www.zhihu.com/login/email"
        post_data = {
            "_xsrf": get_xsrf(),
            "email": account,
            "password": password
        }

    html = session.post(post_url, data=post_data, headers=headers)
    session.cookies.save()

# get_index()
# print is_login()
# print get_captcha()
# print get_xsrf()
# zhihu_login("13175810927", "5PN-Dsu-BMg-RLf")