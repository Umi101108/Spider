# coding: utf8
"""命令行火车票查看器

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2018-02-12
    tickets -dg 成都 南京 2018-02-21
"""
import requests
import time
from prettytable import PrettyTable
from docopt import docopt
from station import station

class TrainsCollection(object):
	

	def __init__(self):
		"""查询到的火车班次集合
		:param available_trains: 一个列表，包含可获得的火车班次，每个火车班次是一个字典
		:param options: 查询的选项，如高铁、动车等
		"""
		self.reverse_station = {v:k for k, v in station.iteritems()}
		self.base_url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes=ADULT'
		self.header = '车次 车站 时间 历时 商务座 一等 二等 软卧 硬卧 硬座 无座'.split()
		self.show_list = 'station_train_code station_interval time_interval lishi swz_num ydz_num edz_num rw_num yw_num yz_num wz_num'.split()
		self.ticket_list = 'swz_num ydz_num edz_num rw_num yw_num yz_num wz_num'.split()


	def all_trains(self, available_trains):
		trains = []
		for raw_train in available_trains:
			data = raw_train.split('|')
			train = {
				'station_train_code': data[3],  # 列车号
				'start_station_telecode': data[4],  # 起始站编码
				'start_station_name': self.reverse_station[data[4]], # 起始站名称
				'end_station_telecode': data[5],  # 终点站编码
				'end_station_name': self.reverse_station[data[5]],  # 终点站名称
				'from_station_telecode': data[6],  # 出发站编码
				'from_station_name': self.reverse_station[data[6]],  # 出发站名称
				'to_station_telecode': data[7],  # 到达站编码
				'to_station_name': self.reverse_station[data[7]],  # 到达站名称
				'station_interval': self.reverse_station[data[6]] + '-' + self.reverse_station[data[7]],  # 行程区间
				'start_time': data[8],  # 出发时间
				'arrive_time': data[9],  # 到达时间
				'time_interval': data[8] +'-'+ data[9],  # 时间区间
				'lishi': data[10],  # 历时
				'canWebBuy': data[11],
				'start_train_date': data[13],
				'rw_num': data[23],  # 软卧
				'wz_num': data[26],  # 无座
				'yw_num': data[28],  # 硬卧
				'yz_num': data[29],  # 硬座
				'edz_num': data[30],  # 二等座
				'ydz_num': data[31],  # 一等座
				'swz_num': data[32],  # 商务座
				'gjrw': data[33]
			}
			trains.append(train)
		return trains
		
	def pretty_print(self, trains):
		pt = PrettyTable()
		pt._set_field_names(self.header)
		for train in trains:
			l = []
			for col in self.show_list:
				l.append(train.get(col))
			pt.add_row(l)
		print pt

	def turn_to_list(self, train):
		l = []
		for col in self.show_list:
			l.append(train.get(col))
		return l

	def print_train_information(self, train):
		string = "{station_train_code}列车，{station_interval}，时间{time_interval}，历时{lishi}，还有余票，赶快抢！".format(
			station_train_code = train.get('station_train_code'),
			station_interval = train.get('station_interval'),
			time_interval = train.get('time_interval'),
			lishi = train.get('lishi'),
		)
		string = string.decode('utf8')+ u'车票信息：' + u'， '.join(map(lambda col: col+' '+train.get(col), [col for col in self.ticket_list if train.get(col)!=u'无' and train.get(col)!='']))
		return string

	def filter_trains(self, trains, options=[], begin_time=0, end_time=24):
		filter_trains = []
		for train in trains:
			if not options or train.get('station_train_code')[0] in options:
				tickets_left = 0
				for col in self.ticket_list:
					if train.get(col) != u'无' and train.get(col) != '':
						tickets_left = 1
				if tickets_left:
					if int(train.get('start_time').split(':')[0]) >= begin_time and int(train.get('arrive_time').split(':')[0]) < end_time:
						# print str(self.turn_to_list(train)).decode('string_escape')
						filter_trains.append(train)
		return filter_trains

	def get_result(self, from_station='上海', to_station='杭州', date='2018-02-12'):
		attempts = 0
		success = False
		while attempts < 10 and not success:
			try:
				url = self.base_url.format(date=date, from_station=station.get(from_station), to_station=station.get(to_station))
				response = requests.get(url, verify=False)
				print url
				result = response.json()['data']['result']
				return result
			except:
				attempts += 1
				if attempts == 10:
					return []
				time.sleep(2)

	def main(self, from_station='上海', to_station='杭州', date='2018-02-12', options=[]):
		result = self.get_result(from_station, to_station, date)
		trains = self.all_trains(result)
		if trains != []:
			trains = self.filter_trains(trains, options)
			return trains
		else:
			print  '请求失效'



if __name__ == '__main__':
	arguments = docopt(__doc__)
	from_station = arguments['<from>']
	to_station = arguments['<to>']
	date = arguments['<date>']
	options = [key[-1].upper() for key, value in arguments.items() if value is True]
	TrainsCollection().main(from_station, to_station, date, options)
