# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2017/8/14 下午7:56'

import hashlib

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()
