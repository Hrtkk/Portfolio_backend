from bson.json_util import dumps
import json
import datetime


Transactions = [
  {'TransactionID': 124582, 'TransactionDate': '2002-06-01', 'StockId': 1, 'TransactionFlag': 'B', 'NumberOfShares': 85},
  {'TransactionID': 124578, 'TransactionDate': '2001-06-01', 'StockId': 3, 'TransactionFlag': 'B', 'NumberOfShares': 125},
  {'TransactionID': 124712, 'TransactionDate': '2004-06-01', 'StockId': 3, 'TransactionFlag': 'B', 'NumberOfShares': 225},
  {'TransactionID': 124810, 'TransactionDate': '2004-06-01', 'StockId': 4, 'TransactionFlag': 'B', 'NumberOfShares': 125},
  {'TransactionID': 125178, 'TransactionDate': '2004-06-01', 'StockId': 6, 'TransactionFlag': 'B', 'NumberOfShares': 25},
  {'TransactionID': 126578, 'TransactionDate': '2005-06-01', 'StockId': 5, 'TransactionFlag': 'B', 'NumberOfShares': 525},
  {'TransactionID': 127518, 'TransactionDate': '2005-06-01', 'StockId': 7, 'TransactionFlag': 'B', 'NumberOfShares': 125},
  {'TransactionID': 127528, 'TransactionDate': '2005-06-01', 'StockId': 2, 'TransactionFlag': 'B', 'NumberOfShares': 525},
  {'TransactionID': 127573, 'TransactionDate': '2006-06-01', 'StockId': 2, 'TransactionFlag': 'S', 'NumberOfShares': -425},
  {'TransactionID': 128598, 'TransactionDate': '2007-06-01', 'StockId': 5, 'TransactionFlag': 'S', 'NumberOfShares': -325},
  {'TransactionID': 134578, 'TransactionDate': '2011-06-01', 'StockId': 3, 'TransactionFlag': 'S', 'NumberOfShares': -205},
  {'TransactionID': 134582, 'TransactionDate': '2012-06-01', 'StockId': 1, 'TransactionFlag': 'S', 'NumberOfShares': -145},
  {'TransactionID': 134674, 'TransactionDate': '2013-06-01', 'StockId': 4, 'TransactionFlag': 'S', 'NumberOfShares': -185},
  {'TransactionID': 144712, 'TransactionDate': '2014-06-01', 'StockId': 3, 'TransactionFlag': 'B', 'NumberOfShares': 425},
  {'TransactionID': 144810, 'TransactionDate': '2014-06-01', 'StockId': 4, 'TransactionFlag': 'S', 'NumberOfShares': -25},
  {'TransactionID': 145178, 'TransactionDate': '2014-06-01', 'StockId': 6, 'TransactionFlag': 'B', 'NumberOfShares': 125},
  {'TransactionID': 146578, 'TransactionDate': '2015-06-01', 'StockId': 5, 'TransactionFlag': 'S', 'NumberOfShares': -125},
  {'TransactionID': 157518, 'TransactionDate': '2015-06-01', 'StockId': 7, 'TransactionFlag': 'B', 'NumberOfShares': 25},
  {'TransactionID': 157528, 'TransactionDate': '2015-06-01', 'StockId': 2, 'TransactionFlag': 'S', 'NumberOfShares': -25},
  {'TransactionID': 157573, 'TransactionDate': '2016-06-01', 'StockId': 2, 'TransactionFlag': 'B', 'NumberOfShares': 25},
  {'TransactionID': 158577, 'TransactionDate': '2016-06-01', 'StockId': 2, 'TransactionFlag': 'B', 'NumberOfShares': 75},
  {'TransactionID': 168598, 'TransactionDate': '2017-06-01', 'StockId': 5, 'TransactionFlag': 'S', 'NumberOfShares': -25},

];

# Transactions.sort(key=lambda x: x['TransactionDate'], reverse=True)
# for i in Transactions:
#   print(i)


stocks = set()
stocks_info = dict()
T = dumps(Transactions)
for trans in list(json.loads(T)):
  date = datetime.datetime.strptime(trans['TransactionDate'], '%Y-%m-%d').date()
  if trans['StockId'] not in stocks:
    stocks.add(trans['StockId'])
    stocks_info[trans['StockId']] = []
  stocks_info[trans['StockId']].append([trans['NumberOfShares'], trans['TransactionFlag'], date])
for i in stocks_info:
  print(i)
  stocks_info[i].sort(key=lambda x: x[2])
  # print(stocks_info[i])
  minBal = 0
  bal = 0
  for j in stocks_info[i]:
    print(j)
    
    bal += j[0]
    if minBal > bal:
      minBal = bal

  if minBal < 0:
    print('yes')
    date = datetime.datetime.strptime('2000-01-01', '%Y-%m-%d').date()      
    stocks_info[i].append([(-1*minBal), 'Init', date])
  stocks_info[i].sort(key=lambda x: x[2])
  
  for j in stocks_info[i]:
    print(j)
  print()
  print()
 


