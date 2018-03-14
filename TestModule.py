#!/usr/bin/python3
#coding:utf8
from RedisService import redisService
def testRedis():
	print('str')
	redisService.set('string','str')
	print(redisService.keys('s*'))
	print(redisService.get('string'))
	print('list')
	redisService.rpush('list',1)
	redisService.rpush('list',2)
	redisService.rpush('list',3)
	redisService.rpush('list',3)
	print(redisService.lrange('list',0,-1))
	print('set')
	redisService.sadd('set',1)
	redisService.sadd('set',2)
	redisService.sadd('set',3)
	redisService.sadd('set',3)
	print(redisService.smembers('set'))
	
if __name__=='__main__':
	#testRedis()