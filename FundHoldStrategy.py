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
from DateTimeUtils import dateTimeUtils
class FundHoldStrategy():
	strategyName='fund_hold'
	buyKey='buy:fund_hold'
	sellKey='sell:fund_hold'
	compare_last_increment=30
	fund_hold_rate=30
	def __init__(self):
		pass
			
	def strategy(self):
		try:
			calc_year,cal_quarter=dateTimeUtils.getCalYearAndQuarter()
			df=ts.fund_holdings(calc_year,cal_quarter)
			for index,row in df.iterrows():
				code=row.code
				#同上期相比，基金在增仓，且增幅大于50%
				nlast=float(row.nlast)
				#基金持股流通占比大于30%
				ratio=float(row.ratio)
				if nlast > self.compare_last_increment and ratio > self.fund_hold_rate:
					redisService.sadd(self.buyKey,code)
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

fundHoldStrategy=FundHoldStrategy()

if __name__=='__main__':
	print("基金持股策略开始时间：",datetime.datetime.now().strftime(Config.DATE_TIME_FORMAT_STR))
	fundHoldStrategy.clearRedis()
	fundHoldStrategy.strategy()
	emailContent=fundHoldStrategy.getEmailContent()
	if emailContent :
		#发送结果邮件
		EmailService.sendTextOrHtml('基金持股策略结果',emailContent,['yantaozhou@qq.com'])
	else:
		print('基金持股策略结束，无需发送邮件')
	#清理redis缓存
	fundHoldStrategy.clearRedis()
	print("基金持股策略结束时间：",datetime.datetime.now().strftime(Config.DATE_TIME_FORMAT_STR))