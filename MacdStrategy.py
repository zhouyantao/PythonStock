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
class MacdStrategy():
	strategyName='MACD'
	buyKey='buy:MACD'
	sellKey='sell:MACD'
	dateDelta=52
	def __init__(self):
		pass
	#计算快速平滑移动均线
	def cal_EMA(self,df,EMA_days,days):
		#当前收盘价
		close=float(df.ix[EMA_days-days,:].close)
		#递归结束条件（如果计算天数为1时，则返回df的行数为12+2的收盘价(第一个EMA取前一日收盘价)）
		if 1 >= days :
			return float(df.ix[EMA_days+2,:].close)
		return 2*close/(EMA_days+1) + (EMA_days-1)*self.cal_EMA(df,days-1)/(EMA_days+1)
		
	def cal_DEA(self,df):
		sum=0
		for num in range(0,9):
			EMA=cal_EMA(df,num+1,num+1)
			sum=sum+EMA
		return sum/9
		
	def strategy(self,stockNo):
		if stockNo is not None:
			try:
				nowDate=datetime.datetime.now()
				endDateStr=nowDate.strftime(Config.FORMAT_STR)
				startDateStr=(nowDate-datetime.timedelta(days=self.dateDelta)).strftime(Config.FORMAT_STR)
				df = ts.get_hist_data(stockNo,start=startDateStr,end=endDateStr) 
				#最少需要28行数据
				if df and (len(df.index) >= 28) :
					front_EMA12=cal_EMA(df.ix[1:-1,:],12,12)
					front_EMA26=cal_EMA(df.ix[1:-1,:],26,26)
					#前日差离率
					front_DIF=EMA12-EMA26
					EMA12=cal_EMA(df,12,12)
					EMA26=cal_EMA(df,26,26)
					#今日差离率
					DIF=EMA12-EMA26
					DEA=cal_DEA(df)
					BAR=2*(DIF-DEA)
					#根据离差率判断是否属于上升趋势
					if front_DIF < DIF and DIF >= DEA :
						#如果离差率上穿DEA则为金叉，发出买入信号
						#存入买入股票编码
						redisService.sadd(self.buyKey,stockNo)
					#如果离差率下破DEA则为死叉，发出卖出信号
					if front_DIF > DIF and DIF <= DEA :
						#如果当前股票在持股里面，则发出卖出信号
						holdStocks=redisService.smembers(Config.KEY_HOLD_STOCK)
						for holdNo in holdStocks:
							if holdNo == stockNo :
								redisService.sadd(self.sellKey,stockNo)
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

macdStrategy=MacdStrategy()

if __name__=='__main__':
	print('请确保当日收盘后再运行，否则需要调整历史行情数据的获取截止日期为前一天')
	print("MACD策略开始时间：",datetime.datetime.now().strftime(Config.DATE_TIME_FORMAT_STR))
	macdStrategy.clearRedis()
	stockNos=stockService.getStockCodes()
	for index in range(0,len(stockNos)):
		stockNo=stockNos[index]
		macdStrategy.strategy(stockNo)
	emailContent=macdStrategy.getEmailContent()
	if emailContent :
		#发送结果邮件
		EmailService.sendTextOrHtml('MACD策略结果',emailContent,['yantaozhou@qq.com'])
	else:
		print('MACD策略结束，无需发送邮件')
	#清理redis缓存
	macdStrategy.clearRedis()
	print("MACD策略结束时间：",datetime.datetime.now().strftime(Config.DATE_TIME_FORMAT_STR))