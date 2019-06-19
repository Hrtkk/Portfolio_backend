from pymongo import MongoClient
from bson.json_util import dumps
import json
import datetime

client = MongoClient()
db = client.angularFlask
user = db.usersDB
transaction = db.transactionsDb
ticker = db.ticker
customerId=1
def sortSecond(val): 
    return val[0]  


while customerId < 2:
	stocks = set()
	stocks_info = dict()
	T = dumps(transaction.find({'CustomerId':customerId}))
	for trans in list(json.loads(T)):
		date = datetime.datetime.strptime(trans['TransactionDate'], '%Y-%m-%d').date()
		if trans['StockId'] not in stocks:
			stocks.add(trans['StockId'])
			stocks_info[trans['StockId']] = []
		stocks_info[trans['StockId']].append([trans['NumberOfShares'], trans['TransactionFlag'], date])
	for i in stocks_info:
		stocks_info[i].sort(key=lambda x: x[2])
		minBal = 0
		bal = 0
		for j in stocks_info[i]:
			bal += stocks_info[i][0]
			if minBal > bal:
				minBal = bal
		if minBal < 0:
			date = datetime.datetime.strptime('2000-01-01', '%Y-%m-%d').date()			
			stocks_info[i].append(minBal, 'Init', date)
		stocks_info[i].sort(key=lambda x: x[2])

	customerId += 1


