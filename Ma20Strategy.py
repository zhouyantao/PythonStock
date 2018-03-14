#!/usr/bin/python  
# coding: UTF-8
import sys   
import tushare as ts  
import time
import datetime
import Signal
import Config
import EmailService
from RedisService import redisService
from StockService import stockService
class Ma20Strategy():
	strategyName='ma20'
	buyKey='buy:ma20'
	sellKey='sell:ma20'
	dateDelta=7
	def __init__(self):
		pass
	def strategy(self,stockNo):
		if stockNo is not None:
			try:
				nowDate=datetime.datetime.now()
				endDateStr=nowDate.strftime(Config.FORMAT_STR)
				startDateStr=(nowDate-datetime.timedelta(days=self.dateDelta)).strftime(Config.FORMAT_STR)
				df = ts.get_hist_data(stockNo,start=startDateStr,end=endDateStr) 
				if (df is not None) and (len(df.index) >= self.dateDelta):
					ma20 = df[u'ma20']
					close = df[u'close']
					underline=True
					for index in range(1,self.dateDelta-1):
						if close[index] > ma20[index]:
							underline=False
							break
					if underline and close[0] > ma20[0]:
						#存入买入股票编码
						redisService.sadd(self.buyKey,stockNo)
						return Signal.Signal(stockNo=stockNo,buy=True,dateStr=endDateStr)
					upline=True
					for index in range(1,self.dateDelta-1):
						if close[index] < ma20[index]:
							upline=False
							break
					if upline and close[0] < ma20[0]:
						#存入买入股票编码
						redisService.sadd(self.sellKey,stockNo)
						return Signal.Signal(stockNo=stockNo,sell=True,dateStr=dateStr)				
					#如果前3天的收盘价在20天均线下方，而当前收盘价在均线上方，则发出买入信号
					# if close[1] < ma20[1] and close[2] < ma20[2] and close[3] < ma20[3] and close[0] > ma20[0] :
						#存入买入股票编码
						# redisService.sadd(self.buyKey,stockNo)
						# return Signal.Signal(stockNo=stockNo,buy=True,dateStr=dateStr)
					#如果前3天的收盘价在20天均线上方，而当前收盘价在均线上方，则发出买入信号
					# if close[1] > ma20[1] and close[2] > ma20[2] and close[3] > ma20[3] and close[0] < ma20[0] :
						# redisService.sadd(self.sellKey,stockNo)
						# return Signal.Signal(stockNo=stockNo,sell=True,dateStr=dateStr)
				return None
			except:
				print(self.strategyName,"策略出现异常:", sys.exc_info()[0])
			finally:
				#让出线程
				time.sleep(1)
				return None
		return None
			
	def getEmailContent(self):
		content=None
		buyList=redisService.smembers(self.buyKey)
		sellList=redisService.smembers(self.sellKey)
		if len(buyList) > 0 or len(sellList) > 0 :
			content='策略名称：' + self.strategyName
			content=content+'<br/>'
			content=content+'买入('+str(len(buyList))+'支)：<br/>'
			content = content + ','.join(buyList)
			content=content+'\r\n'
			content=content+'卖出('+str(len(sellList))+'支)：<br/>'
			content = content + ','.join(sellList)
		return content
		
	def clearRedis(self):
		redisService.delete(self.buyKey)
		redisService.delete(self.sellKey)

ma20Strategy=Ma20Strategy()

if __name__=='__main__':
	print("Ma20策略开始时间：",datetime.datetime.now().strftime(Config.DATE_TIME_FORMAT_STR))
	ma20Strategy.clearRedis()
	stockNos=stockService.getStockCodes()
	for index in range(0,len(stockNos)):
		stockNo=stockNos[index]
		ma20Strategy.strategy(stockNo)
	emailContent=ma20Strategy.getEmailContent()
	if emailContent :
		#发送结果邮件
		EmailService.sendTextOrHtml('Ma20策略结果',emailContent,['yantaozhou@qq.com'])
	else:
		print('Ma20策略结束，无需发送邮件')
	#清理redis缓存
	ma20Strategy.clearRedis()
	print("Ma20策略结束时间：",datetime.datetime.now().strftime(Config.DATE_TIME_FORMAT_STR))