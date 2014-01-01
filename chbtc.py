#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import commands
import json

'''
    Trade API for chbtc.com

    http://donge.org
    donge@donge.org
'''

access_key="YOUR-ACCESS_KEY"
root_url = "https://trade.chbtc.com/api/"

class Chbtc(object):
    def __init__(self):
    	pass

    def getMarket(self):
		r = requests.get('http://api.chbtc.com/data/ticker')
		ret = r.json()
		return ret['ticker']['sell'], ret['ticker']['buy'], ret['ticker']['last']

    def sellBtc(self, price, amount):
        prefix = "method=order&accesskey="+access_key+"&price="+str(price)+"&amount="+str(amount)+"&tradeType=0&currency=btc"
        postfix = self.getPostfix(prefix)
        url = root_url + "order?" + prefix + postfix
        r = requests.post(url)
        ret = r.json()
        #print ret
        return ret['message'] #success

    def buyBtc(self, price, amount):
    	prefix = "method=order&accesskey="+access_key+"&price="+str(price)+"&amount="+str(amount)+"&tradeType=1&currency=btc"
        postfix = self.getPostfix(prefix)
        url = root_url + "order?" + prefix + postfix
        r = requests.post(url)
        ret = r.json()
        #print ret
        return ret['message'] #success

    def cancelAllOrders(self):
    	sid = self.getSellOrders()
    	time.sleep(1) # can not post with in one second
    	bid = self.getBuyOrders()
    	time.sleep(1)
    	if sid != 0:
    		cancelOrder(sid)
            time.sleep(1)
    	if bid != 0:
    		cancelOrder(bid)
            time.sleep(1)
        return sid, bid

    def getSellOrders(self):
    	prefix = "method=getOrders&accesskey="+access_key+"&tradeType=0&currency=btc&pageIndex=1"
        postfix = self.getPostfix(prefix)
    	url = root_url + "getOrders?" + prefix + postfix
    	r = requests.post(url)
        json = r.json()
        #print json
        try:
        	ret = [0]['id']
        except:
        	ret = 0
        return ret

    def getBuyOrders(self):
    	prefix = "method=getOrders&accesskey="+access_key+"&tradeType=1&currency=btc&pageIndex=1"
        postfix = self.getPostfix(prefix)
    	url = root_url + "getOrders?" + prefix + postfix
    	r = requests.post(url)
        json = r.json()
        #print json
        try:
        	ret = [0]['id']
        except:
        	ret = 0
        return ret

    def cancelOrder(self, id):
    	prefix = "method=cancelOrder&accesskey="+access_key+"&id="+str(id)+"&currency=btc"
        postfix = self.getPostfix(prefix)
    	url = root_url + "cancelOrder?" + prefix + postfix
    	r = requests.post(url)
        ret = r.json()
        #print ret
        return ret['message'] #success


    def getAccount(self):
    	prefix = "method=getAccountInfo&accesskey="+access_key
    	postfix = self.getPostfix(prefix)
    	url = root_url + "getAccountInfo?" + prefix + postfix
    	r = requests.post(url)
        ret = r.json()
        return float(ret['result']['balance']['BTC']['amount']), float(ret['result']['balance']['CNY']['amount'])

    def getPostfix(self, param):
    	ret = "&sign=" + self.getSign(param) + "&reqTime=" + self.getMill()
    	#print ret
    	return ret

    def getSign(self, param):
        (status, output) = commands.getstatusoutput('java EncryDigestUtil "' + param +'"')
        return output

    def getMill(self):
    	return str(int(time.time() * 1000))


if __name__=='__main__':

    test = Chbtc()

	print '---get market---'
	print test.getMarket()

	print '---get account---'
	#print test.getAccount()

	print '---get orders---'
	#print test.getSellOrders()
    #print test.getBuyOrders()

	print '---cansel order---'
	#print test.cancelOrder(201401011576851)
	#print test.cancelAllOrders()

	print '---sell---'
	#print test.sellBtc(10000.0, 0.1)

	print '---buy---'
	#print test.buyBtc(0.1, 0.1)

