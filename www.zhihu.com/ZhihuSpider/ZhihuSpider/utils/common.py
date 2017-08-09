# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2017/8/9 下午9:57'


def extract_num(text):
    # 从字符串中提取出数字
    match_re = re.match(".*?(\d+).*?", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums