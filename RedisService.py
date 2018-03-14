#!/usr/bin/python3
#coding:utf8
import redis
import Config

class RedisService():
	__POOL=None
	__DB=None
	def __init__(self):
		if self.__DB is None:
			self.__POOL=redis.ConnectionPool(host=Config.REDIS_HOST,port=Config.REDIS_PORT,db=0,password=Config.REDIS_PASSWD)
			self.__DB=redis.StrictRedis(connection_pool=self.__POOL)
	
	#获取字符串
	def to_str(self,bytes_or_str):
		if isinstance(bytes_or_str,bytes):
			value=bytes_or_str.decode(Config.CHAR_SET)
		else:
			value=bytes_or_str
		return value
	#获取bytes
	def to_bytes(self,bytes_or_str):
		if isinstance(bytes_or_str,str):
			value=bytes_or_str.encode(Config.CHAR_SET)
		else:
			value=bytes_or_str
		return bytes_or_str
	#
	############
	#key 操作
	############
	#
	#
	#是否存在name这个key  True
	def exists(self,key):
		return self.__DB.exists(key)
	#删除name这个key 1
	def delete(self,key):
		return self.__DB.delete(key)
	#判断name这个key类型 str
	def type(self,key):
		return self.to_str(self.__DB.type(key))
	#获取所有以n开头的key ['name']	
	def keys(self,key):
		byteKeys=self.__DB.keys(key)
		keys=[]
		for bKey in  byteKeys :
			keys.append(self.to_str(bKey))
		return keys
	#获取随机的一个key 'name'
	def randomkey(self):
		return self.to_str(self.__DB.randomkey())
	#将name重命名为nickname
	def rename(self,name,nickname):
		return self.__DB.rename(name,nickname)
	#获取当前数据库中key的数目 100
	def dbsize(self):
		return self.__DB.dbsize()
	#将name这key的过期时间设置2秒 True
	def expire(self,key,time):
		return self.__DB.expire(key,time)
	#获取name这key的过期时间 -1
	def ttl(self,key):
		return self.__DB.ttl(key)
	#将name移动到2号数据库 True	
	def move(self,key,no):
		return self.__DB.move(key,no)		
	#删除当前选择数据库中的所有key True
	def flushdb(self):
		return self.__DB.flushdb()
	#删除所有数据库中的所有key True	
	def flushall(self):
		return self.__DB.flushall()
	#
	############
	#String 操作
	############
	#
	#
	#给name这个key的value赋值为Bob True	
	def set(self,key,value):
		return self.__DB.set(key,value)
	#将name移动到2号数据库 True	
	def get(self,key):
		return self.to_str(self.__DB.get(key))
	#赋值name为Mike并得到上次的value 'Bob'	
	def getset(self,key,value):
		return self.to_str(self.__DB.getset(key,value))
	#返回name和nickname的value ['Mike','Miker']	
	def mget(self,*keys):
		bValues=self.__DB.mget(keys)
		values=[]
		for bValue in bValues:
			values.append(self.to_str(bValue))
		return values
	#如果newname这key不存在则设置值为James 第一次运行True，第二次False	
	def setnx(self,key,value):
		return self.__DB.setnx(key,value)
	#将name这key的值设为James，有效期1秒 True	
	def setex(self,key,time,value):
		return self.__DB.setex(key,time,value)
	#设置name为Hello字符串，并在index为6的位置补World  11，修改后的字符串长度	
	def setrange(self,key,index,insert):
		return self.__DB.setrange(key,index,insert)
	#将name1设为Durant，name2设为James True	
	def mset(self,dict):
		return self.__DB.mset(dict)
	#在name3和name4均不存在的情况下才设置二者值 True	
	def msetnx(self,dict):
		return self.__DB.msetnx(dict)
	#age对应的值增1，若不存在则会创建并设置为1 1，即修改后的值	
	def incr(self,key,index):
		return self.__DB.incr(key,index)
	#age对应的值减1，若不存在则会创建并设置为-1 -1，即修改后的值
	def decr(self,key,index):
		return self.__DB.decr(key,index)
	#向key为nickname的值后追加OK，即修改后的字符串长度	
	def append(self,key,insert):
		return self.__DB.append(key,insert)
	#4)	返回key为name的值的字符串，截取索引为1-4的字符 'ello'	
	def substr(self,key,start,end):
		return self.to_str(self.__DB.substr(key,start,end))
	#返回key为name的值的字符串，截取索引为1-4的字符 'ello'
	def getrange(self,key,start,end):
		return self.to_str(self.__DB.getrange(key,start,end))
	#
	############
	#List 操作
	############
	#
	#
	#给list这个key的list尾添加元素 list 大小	
	def rpush(self,key,*values):
		return self.__DB.rpush(key,*values)
	#给list这个key的list头添加 list 大小		
	def lpush(self,key,value):
		return self.__DB.lpush(key,value)
	#返回key为list的列表的长度 4	
	def llen(self,key):
		return self.__DB.llen(key)
	#返回起始为1终止为3的索引范围对应的list	
	def lrange(self,key,start,end):
		bKeys=self.__DB.lrange(key,start,end)
		keys=[]
		for bKey in bKeys:
			keys.append(self.to_str(bKey))
		return keys
	#返回并删除名为list的list第一个元素	
	def lpop(self,key):
		return self.__DB.lpop(key)
	#返回并删除名为list的list最后一个元素	
	def rpop(self,key):
		return self.__DB.rpop(key)
	#
	############
	#Set 操作
	############
	#
	#		
	#向key为name的set中添加元素 添加元素的个数	
	def sadd(self,key,*values):
		return self.__DB.sadd(key,*values)	
	#从key为name的set中删除元素	
	def srem(self,key,*values):
		return self.__DB.srem(key,*values)	
	#返回key为name的set的所有元素
	def smembers(self,key):
		bValues=self.__DB.smembers(key)
		values=[]
		for bValue in bValues:
			values.append(self.to_str(bValue))
		return values
	#
	############
	#Hash 操作
	############
	#
	#
	#向key为name的hash中添加映射  添加元素的个数
	def hset(self,key,field,value):
		return self.__DB.hset(key,field,value)
	#返回key为name的hash中field对应的value  添加元素的个数
	def hget(self,key,field):
		return self.to_str(self.__DB.hget(key,field))
	#key为namehash中是否存在键名为key的映射
	def hexists(self,key,field):
		return self.__DB.hexists(key,field)
	#key为namehash中删除键名为key的映射
	def hdel(self,key,*fields):
		return self.__DB.hdel(key,*fields)
	#从key为name的hash中获取映射个数
	def hlen(self,key):
		return self.__DB.hlen(key,*fields)
	#从key为name的hash中获取所有映射键名
	def hkeys(self,key):
		bFields=self.__DB.hkeys(key)
		fields=[]
		for bField in bFields:
			fields.append(self.to_str(bField))
		return fields
	#从key为name的hash中获取所有映射键值对
	def hgetall(self,key):
		return self.__DB.hgetall(key)
		
redisService=RedisService()