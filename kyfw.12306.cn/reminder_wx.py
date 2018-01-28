# -*- coding: utf-8 -*-
__author__ = 'umi'
__date__ = '2018/1/28 下午5:44'

import re
import time
import itchat

from tickets import TrainsCollection

ticket_list = 'swz_num ydz_num edz_num rw_num yw_num yz_num wz_num'.split()

def print_train_information(train):
    string = "{station_train_code}列车，{station_interval}，时间{time_interval}，历时{lishi}，还有余票，赶快抢！".format(
        station_train_code=train.get('station_train_code'),
        station_interval=train.get('station_interval'),
        time_interval=train.get('time_interval'),
        lishi=train.get('lishi'),
    )
    string = string.decode('utf8') + u'车票信息：' + u'， '.join(map(lambda col: col + ' ' + train.get(col),
                                                               [col for col in ticket_list if
                                                                train.get(col) != u'无' and train.get(col) != '']))
    return  string

def chinese(message):
    return message.replace(u'swz_num', u'商务座').replace(u'ydz_num', u'一等座').replace(u'edz_num', u'二等座')


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    from_station = '上海'
    to_station = '章丘'
    date = '2018-02-12'
    options = [u'G']
    while True:
        trains = TrainsCollection().main(from_station=from_station, to_station=to_station, date=date, options=options)
        if trains and trains != []:
            message = '{} {}-{}的车次情况如下：\n'.format(date, from_station, to_station).decode('utf8')
            for train in trains:
                message += chinese(print_train_information(train)) + '\n'
            print message
            # user = itchat.search_friends(name=u'')
            # itchat.send(message, toUserName=user[0]['UserName'])
            itchat.send(message, toUserName='filehelper')
        time.sleep(5)