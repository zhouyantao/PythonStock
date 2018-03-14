#! /usr/bin/env python
#coding=utf-8
import time
import os
import sched

class SchedulerService():
	# 第一个参数确定任务的时间，返回从某个特定的时间到现在经历的秒数
	# 第二个参数以某种人为的方式衡量时间
	schedule = None
	def __init__(self):
		if self.schedule is None:
			self.schedule=sched.scheduler(time.time, time.sleep)
	
	def perform_command(self,func,after,interval):
		# 安排inc秒后再次运行自己，即周期运行
		self.schedule.enter(interval,0,self.perform_command,(func,after,interval))
		func()
			
	def timming_exe(self,func,after=60,interval=24*60*60):
		# enter用来安排某事件的发生时间，从现在起第n秒开始启动
		self.schedule.enter(after,0,self.perform_command,(func,after,interval))
		# 持续运行，直到计划时间队列变成空为止
		self.schedule.run()
         
schedulerService=SchedulerService()
if __name__=='__main__':
	def printTime():
		print(time.time())
	#每一秒打印一次时间
	schedulerService.timming_exe(printTime,1,1)