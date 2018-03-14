# PythonStock
===============
>使用python的tushare库编写的股票相关的应用,存储使用redis,策略结果和监控结果
通过邮件进行发送,需邮件服务方提供相应的smtp服务器地址及密码(非登录密码，腾讯的为imop授权码) 使用前请先修改Config.py和EmailService中的相关的配置，各个文件作用如下：
## Config.py
>配置文件，控制redis访问配置，及各个Redis中的set的key（如：持有的股票，新股开板监控股票）
## DateTimeUtils.py
>日期时间操作工具类（如：判断是否属于交易时间）
## EmailService.py
>用于发送邮件（请修改相应配置，写的匆忙，没有提取到config中）
## FundHoldStrategy.py
>基金持股选股策略
## HoldStocks.txt
>持有的股票列表，用于持股多时，初始化redis中的持股set
## Ma20Strategy.py
>20日均线策略，遍历市场所有股票，挑选出突破20日均线的为买入股票，否则且为持有股票则为卖出股票
## MacdStrategy.py
>MACD策略
## Main.py
>多策略组合入口
## MonitorStrategy.py
>监控策略，监控持有股票，如果涨幅或跌幅达到5%，则发出邮件提示
## NewStockMonitor.py
>监控持有的新股，如果当前价格低于涨停价（破板）则给出提示
## RedisService.py
>redis操作service
## SchedulerService.py
>python 计划调度工具类
## seleniumTest.py
>python中selenium使用的例子 




