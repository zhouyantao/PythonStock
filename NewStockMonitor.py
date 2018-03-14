#!/usr/bin/python  
# coding: UTF-8   
import sys
import tushare as ts  
import time
import datetime
import Signal
import Config
import EmailService
from SchedulerService import schedulerService
from RedisService import redisService
from StockService import stockService

class NewStockMonitor():
	strategyName='newstock'
	buyKey='buy:newstock'
	sellKey='sell:newstock'
	rate=1
	def __init__(self):
		pass
	def strategy(self):
		needEmail=False
		#非交易时间，直接返回
		if not stockService.isTradeTime():
			return needEmail
		#获取持有的股票
		try:
			holdStocks=redisService.smembers(Config.KEY_NEW_STOCK)
			for stockNo in holdStocks:
				#获取当前股票的实时分笔
				df=ts.get_realtime_quotes(stockNo)
				column_open=df['open']
				open=float(column_open[0])
				column_price=df['price']
				price=float(column_price[0])
				percent=abs(open-price)/open
				#如果当前价格低于开盘价（打开涨停板),则需要给出卖出提示
				if price<open :
					needEmail=True
					redisService.sadd(self.sellKey,stockNo)
		except:
			print(self.strategyName,"策略出现异常:", sys.exc_info()[0])
		finally:
			#让出线程
			time.sleep(1)
			return needEmail
		return needEmail 
			
	def getEmailContent(self):
		content='策略名称：' + self.strategyName
		content=content+'\r\n'
		content=content+'买入：\r\n'
		content = content + ','.join(redisService.smembers(self.buyKey))
		content=content+'\r\n'
		content=content+'卖出：\r\n'
		content = content + ','.join(redisService.smembers(self.sellKey))
		return content
		
	def clearRedis(self):
		redisService.delete(self.buyKey)
		redisService.delete(self.sellKey)
		
	def monitor(self):
		needEmail=self.strategy()
		if needEmail:
			emailContent=self.getEmailContent()
			self.clearRedis()
			#发送结果邮件
			EmailService.sendTextOrHtml('stock监控结果',emailContent,['yantaozhou@qq.com'])
		print('新股开板监控一次',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),'，需要邮件：',needEmail)

newStockMonitor=NewStockMonitor()

if __name__=="__main__" :	
	#每3分钟跑一遍
	schedulerService.timming_exe(newStockMonitor.monitor,after=6,interval=3*60)


