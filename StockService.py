#!/usr/bin/python3  
# coding: UTF-8  
import os
import time
import tushare as ts   
import Config
from RedisService import redisService
class StockService():
	def __init__(self):
		pass
	def getStockDicts():
	# code,代码
	# name,名称
	# industry,所属行业
	# area,地区
	# pe,市盈率
	# outstanding,流通股本(亿)
	# totals,总股本(亿)
	# totalAssets,总资产(万)
	# liquidAssets,流动资产
	# fixedAssets,固定资产
	# reserved,公积金
	# reservedPerShare,每股公积金
	# esp,每股收益
	# bvps,每股净资
	# pb,市净率
	# timeToMarket,上市日期
	# undp,未分利润
	# perundp, 每股未分配
	# rev,收入同比(%)
	# profit,利润同比(%)
	# gpr,毛利率(%)
	# npr,净利润率(%)
	# holders,股东人数
		stocks=[]
		df=ts.get_stock_basics()
		column_code=df[u'code']
		column_name=df[u'name']
		column_industry=df[u'industry']
		column_area=df[u'area']
		column_pe=df[u'pe']
		column_outstanding=df[u'outstanding']
		column_totals=df[u'totals']
		column_totalAssets=df[u'totalAssets']
		return stocks
	def getStockCodes(self):
		df=ts.get_stock_basics()
		return df.index
	
	def isTradeTime(self):
		struct_time=time.localtime()
		tm_wday=struct_time[6]
		tm_hour=struct_time[3]
		tm_min=struct_time[4]
		#周一到周五
		if 0<=tm_wday and tm_wday<=4 :
			if 9<tm_hour or (9==tm_hour and 30 <=tm_min) :
				return True
			if tm_hour>=13 and tm_hour<=15 :
				return True
		return False
	
	def initHoldStocksToRedis(self):
		filePath=os.path.join(os.getcwd(),Config.HOLD_STOCKS_FILE_NAME)
		with open(filePath) as somefile:
			lines=somefile.readlines()
			for line in lines :
				stockNo=line.strip()
				if len(stockNo)>0:
					try:
						redisService.sadd(Config.KEY_HOLD_STOCK,stockNo)
					except:
						pass

stockService=StockService()
if __name__=='__main__':
	stockService.initHoldStocksToRedis()
	print(redisService.smembers(Config.KEY_HOLD_STOCK))
