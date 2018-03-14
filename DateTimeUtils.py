#!/usr/bin/python  
# coding: UTF-8
import time
class DateTimeUtils():
	def __init__(self):
		pass
	def getCurrentQuarter(self):
		localtime=time.localtime()
		month=localtime.tm_mon
		return int(month/3+1)
	
	#获取需要计算的年份和季度数
	def getCalYearAndQuarter(self):
		localtime=time.localtime()
		#获取计算年份
		calc_year=localtime.tm_year
		#获取当前季度
		now_quarter=self.getCurrentQuarter()
		cal_quarter=now_quarter-1
		#如果计算季度为0，则计算年份减1，季度为4
		if 0==cal_quarter:
			cal_quarter=4
			calc_year=calc_year-1
		return (calc_year,cal_quarter)
		
dateTimeUtils=DateTimeUtils()

if __name__=='__main__':
	calc_year,cal_quarter=dateTimeUtils.getCalYearAndQuarter()
	print(calc_year)
	print(cal_quarter)
