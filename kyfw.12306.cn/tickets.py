# coding: utf8
import requests
from prettytable import PrettyTable
from station import station


class TrainsCollection(object):
	

	def __init__(self, available_trains, options):
		"""查询到的火车班次集合
		:param available_trains: 一个列表，包含可获得的火车班次，每个火车班次是一个字典
		:param options: 查询的选项，如高铁、动车等
		"""
		self.available_trains = available_trains
		self.options = options
		self.reverse_station = {v:k for k, v in station.iteritems()}
		self.header = '车次 车站 时间 历时 商务座 一等 二等 软卧 硬卧 硬座 无座'.split()

	@property
	def trains(self):
		for raw_train in self.available_trains:
			data = raw_train.split('|')
			train_no = data[2]
			# print data[3], data[32]
			station_train_code = data[3]
			start_station_telecode = data[4]
			start_station_name = self.reverse_station[start_station_telecode]
			end_station_telecode = data[5]
			end_station_name = self.reverse_station[end_station_telecode]
			from_station_telecode = data[6]
			from_station_name = self.reverse_station[from_station_telecode]
			to_station_telecode = data[7]
			to_station_name = self.reverse_station[to_station_telecode]
			start_time = data[8]
			arrive_time = data[9]
			# day_difference
			# train_class_name
			lishi = data[10]
			canWebBuy = data[11]
			# lishiValue
			# yp_info
			# control_train_day
			start_train_date = data[13]
			# seat_feature
			# yp_ex
			# train_seat_feature
			# seat_type
			# location_code
			# from_station_no
			# to_station_no
			# control_train_day
			# sale_time
			# is_support_card
			# note 
			# controlled_train_flag
			# controlled_train_message
			# gg_num
			# gr_num
			# qt_num
			# rz_num
			# tz_num
			# yb_num
			# ze_num
			# zy_num
			rw_num = data[23]
			wz_num = data[26]
			yw_num = data[28]
			yz_num = data[29]
			edz_num = data[30]
			ydz_num = data[31]
			swz_num = data[32]
			gjrw = data[33]
			train = [station_train_code, from_station_name+'-'+to_station_name, start_time+'-'+arrive_time, lishi, swz_num, ydz_num, edz_num, rw_num, yw_num, yz_num, wz_num]
			# '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'
			# print str(train).decode('string_escape')
			yield train
		
	def pretty_print(self):
		pt = PrettyTable()
		pt._set_field_names(self.header)
		for train in self.trains:
			pt.add_row(train)
		print pt


def cli():
	base_url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes=ADULT'
	from_station = station.get('上海')
	to_station = station.get('杭州')
	url = base_url.format(date='2017-10-28', from_station=from_station, to_station=to_station)
	response = requests.get(url, verify=False)
	result = response.json()['data']['result']
	
	TrainsCollection(result, '2').pretty_print()

cli()