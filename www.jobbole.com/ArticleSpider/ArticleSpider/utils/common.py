# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2017/8/6 下午7:44'

import hashlib
import re

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == "__main__":
    print get_md5(u"http://jobbole.com")