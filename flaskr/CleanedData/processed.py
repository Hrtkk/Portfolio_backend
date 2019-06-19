#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 13:54:20 2019

@author: hritik
"""

import pandas as pd
cust_db = pd.read_csv('CustomerDb.csv')
trans = pd.read_csv('StockTransactions.csv')
cust_db1 = cust_db.sort_values(by = ['CustomerId']).to_dict()
tran_1 = trans.sort_values(by = ['CustomerId']).to_dict()
q = trans.sort_values(by = ['CustomerId'])
i=1
j=0
prev = tran_1['CustomerId'][0]
tran_1['CustomerId']
type(tran_1)
tran_1['CustomerId'][65849]
k = 0
p=1
prev = 22
for i in tran_1['CustomerId']:
    print(tran_1['CustomerId'][i])
    if prev == tran_1['CustomerId'][i]:
        tran_1['CustomerId'][i] = p
    else:
        p += 1
        prev = tran_1['CustomerId'][i]
        tran_1['CustomerId'][i] = p
        
tr = pd.DataFrame.from_dict(tran_1)
p = tr.sort_values(by = ['CustomerId'])


k=1
for i in cust_db1['CustomerId']:
    print(cust_db1['CustomerId'][i])
    cust_db1['CustomerId'][i] = k
    k+=1
   
q = pd.DataFrame.from_dict(cust_db1)
p.to_csv('./Tran.csv')
q.to_csv('./Cust.csv')