#!/usr/bin/python  
# coding: UTF-8  
class Signal():
	stockNo=None
	buy=None
	sell=None
	dateStr=None
	def __init__(self,stockNo=None,buy=None,sell=None,dateStr=None):
		self.stockNo=stockNo
		self.buy=buy
		self.sell=sell
		self.dateStr=dateStr