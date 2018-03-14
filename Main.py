#!/usr/bin/python  
# coding: UTF-8
import time
import threading
import EmailService
from SchedulerService import schedulerService
from Ma20Strategy import ma20Strategy
from MonitorStrategy import monitorStrategy
from StockService import stockService
def getStockNos():
#	return ['600050']
	return stockService.getStockCodes()
	
def getStrategies():
	return [ma20Strategy]
	
def func():
	#如果是交易时间，则直接返回
	if stockService.isTradeTime():
		print('交易时间，不执行非实时策略')
		return None
	strategies=getStrategies()
	stockNos=getStockNos()
	emailContent=''
	for strategy in strategies :
		for index in range(0,len(stockNos)):
			stockNo=str(stockNos[index])
			strategy.strategy(stockNo)
		emailContent=emailContent+strategy.getEmailContent()
		strategy.clearRedis()
	#发送结果邮件
	EmailService.sendTextOrHtml('stock策略结果',emailContent,['yantaozhou@qq.com'])

def monitor():
	needEmail=monitorStrategy.strategy()
	if needEmail:
		emailContent=monitorStrategy.getEmailContent()
		monitorStrategy.clearRedis()
		#发送结果邮件
		EmailService.sendTextOrHtml('stock监控结果',emailContent,['yantaozhou@qq.com'])
	print('监控一次',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
#非实时
def strategyScheduler():
	schedulerService.timming_exe(func,after=5)
#实时
def monitorScheduler():
	schedulerService.timming_exe(monitor,after=6,interval=5*60)


threads=[]
strategyThread=threading.Thread(target=strategyScheduler)
#monitorThread=threading.Thread(target=monitorScheduler)
threads.append(strategyThread)
#threads.append(monitorThread)
for thread in threads :
	thread.setDaemon(True)  
	thread.start()
for thread in threads :
	thread.join()
print("执行结束了。\n")


