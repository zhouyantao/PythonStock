#coding:utf-8
from twilio.rest import Client
#认证信息在 twilio 账户里可以找到
def sendMessage(phone,content):
	if phone is not None and content is not None :
		account_sid="ACe4abe0a807da292b15e725ef559a7d24"
		auth_token="1ea0c9fea15531ddd3290f8d8c3a3ec7"
		twilio_phone="+12523022221"
		client=Client(account_sid,auth_token)
		message=client.api.account.messages.create(to="+86"+phone,from_=twilio_phone,body=content)
		if message is not None :
			print("短信发送编号：",message.sid,"发送内容：",content)


if __name__=="__main__" :
	sendMessage('123456','人生苦短，我用python!')