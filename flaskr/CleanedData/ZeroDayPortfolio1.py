#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 10:58:12 2019

@author: hritik
"""
import pandas as pd


df = pd.read_csv('Tran.csv', parse_dates=['trans_date'])
df.head()
min_custId = df['customer_id'].min()
max_custId = df['customer_id'].max()

trans_list = []
for i in df.iterrows():
    trans_list.append(i[1].to_dict())

new_list = []
index = df['no'].max()
for cust_id in range(min_custId, max_custId+1):
    print(cust_id)
    elem = filter(lambda x: x['customer_id'] == cust_id, trans_list)
    Transactions = []
    for j in elem:
        Transactions.append(j)
        
    stocks = set()
    stocks_info = dict()
    for trans in Transactions:
      date = trans['trans_date'].date().strftime('%Y-%m-%d')
      if trans['StockId'] not in stocks:
        stocks.add(trans['StockId'])
        stocks_info[trans['StockId']] = []
      stocks_info[trans['StockId']].append([trans['tran_amount'], trans['TransactionFlag'], date])
    for stk_id in stocks_info:
      #print(stk_id)
      stocks_info[stk_id].sort(key=lambda x: x[2])
      # print(stocks_info[i])
      minBal = 0
      bal = 0
      for j in stocks_info[stk_id]:
      #  print(j)
        
        bal += j[0]
        if minBal > bal:
          minBal = bal
    
      if minBal < 0:
       # print('yes')
        date = datetime.datetime.strptime('2007-01-03', '%Y-%m-%d').date().strftime('%Y-%m-%d')
        index += 1
        new_list.append({'StockId':stk_id,
                         'TransactionFlag':'init',
                         'TransactionId':00000,
                         'customer_id':cust_id,
                         'no':index,
                         'tran_amount':-1*minBal,
                         'trans_date':date,
                         })
        
        stocks_info[stk_id].append([(-1*minBal), 'Init', date])
      stocks_info[stk_id].sort(key=lambda x: x[2])
      
      #for j in stocks_info[stk_id]:
      #  print(j)
      #print()
      #print()

final_Trans =  trans_list + new_list
a = pd.DataFrame(final_Trans)
a.to_csv('Trans2.csv')
     
