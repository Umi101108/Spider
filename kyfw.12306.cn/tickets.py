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
    tickets 北京 上海 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""
import requests
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


	def trains(self, available_trains, options=[]):
		for raw_train in available_trains:
			data = raw_train.split('|')
			train_no = data[2]
			station_train_code = data[3]  # 列车号
			train_type = station_train_code[0]  # 车型
			if not options or train_type in options:
				start_station_telecode = data[4]  # 起始站编码
				start_station_name = self.reverse_station[start_station_telecode]  # 起始站名称
				end_station_telecode = data[5]  # 终点站编码
				end_station_name = self.reverse_station[end_station_telecode]  # 终点站
				from_station_telecode = data[6]  # 出发站编码
				from_station_name = self.reverse_station[from_station_telecode]  # 出发站名称
				to_station_telecode = data[7]  # 到达站编码
				to_station_name = self.reverse_station[to_station_telecode]  # 到达站名称
				start_time = data[8]  # 出发时间
				arrive_time = data[9]  # 到达时间
				lishi = data[10]  # 历时
				canWebBuy = data[11]
				start_train_date = data[13]
				rw_num = data[23]  # 软卧
				wz_num = data[26]  # 无座
				yw_num = data[28]  # 硬卧
				yz_num = data[29]  # 硬座
				edz_num = data[30]  # 二等座
				ydz_num = data[31]  # 一等座
				swz_num = data[32]  # 商务座
				gjrw = data[33]
				train = [station_train_code, from_station_name+'-'+to_station_name, start_time+'-'+arrive_time, lishi, swz_num, ydz_num, edz_num, rw_num, yw_num, yz_num, wz_num]
				# print str(train).decode('string_escape')
				yield train
		
	def pretty_print(self, trains):
		pt = PrettyTable()
		pt._set_field_names(self.header)
		for train in trains:
			pt.add_row(train)
		print pt

	def main(self, from_station='上海', to_station='杭州', date='2018-02-12', options=[]):
		url = self.base_url.format(date=date, from_station=station.get(from_station), to_station=station.get(to_station))
		response = requests.get(url, verify=False)
		result = response.json()['data']['result']
		trains = self.trains(result, options)
		self.pretty_print(trains)


if __name__ == '__main__':
	arguments = docopt(__doc__)
	from_station = arguments['<from>']
	to_station = arguments['<to>']
	date = arguments['<date>']
	options = [key[-1].upper() for key, value in arguments.items() if value is True]
	TrainsCollection().main(from_station, to_station, date, options)
