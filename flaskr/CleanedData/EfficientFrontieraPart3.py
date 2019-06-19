#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 14:03:44 2019

@author: hritik
"""
from collections import defaultdict
import pandas as pd
import quandl

data = pd.read_csv('Stockdata.csv')
data = pd.read_csv('Stock_table.csv')
trans = pd.read_csv('Trans2.csv')
ticker = pd.read_csv('ticker.csv')
risk_profile = pd.read_csv('riskprofile.csv')
ticker = [x for x in ticker['symbol']]


quandl.ApiConfig.api_key = 'k44yWd6JYdYJ4atkfx64'
data = quandl.get_table('WIKI/PRICES', ticker= ticker,
                        qopts = {'columns': ['date', 'ticker', 'adj_close']},
                        date = {'gte': '2007-1-1', 'lte': '2017-01-1'}, paginate=True)

# reorganise data pulled by setting date as index with
# columns of tickers and their corresponding aadjusted prices
clean = data.set_index('date')
table = clean.pivot(columns='ticker')
table = pd.read_csv('Stockdata.csv')
data.drop(columns="Unnamed: 0", inplace =True)
data.drop(columns="None", inplace =True)


frame = pd.to_datetime(table.index)
table.index = frame
grouped_table = table.groupby(pd.Grouper(freq = "3M")).std()
grouped_table.hist()
a = grouped_table.describe()
l = list()
for i in grouped_table:
    l.append(i[1])
p = pd.DataFrame(index = l)
for i in grouped_table:
    p.loc[i[1],0] = grouped_table[i].max() - grouped_table[i].min() 
    p.loc[i[1],1] = grouped_table[i].max()
    p.loc[i[1],2] = grouped_table[i].min() 
p.rename(columns={0:"STD_DIFF",1:"MAX",2:"MIN"}, inplace=True)
p.hist()
p["MIN"].value_counts()


bins = [0, 3, 5, 10, 14, 200]
p['binned'] = pd.cut(p["STD_DIFF"], bins, labels=["Conservative", "Balanced", "Assertive", "Aggressive", "Very Aggressive"])
bins2 = [0, 26, 41, 53, 66, 100]
risk_profile['binned'] = pd.cut(risk_profile["Total"], bins2, labels=["Conservative", "Balanced", "Assertive", "Aggressive", "Very Aggressive"])

p['symbol'] = p.index
q = pd.merge(ticker, p, on="symbol")
trans.drop(columns=['Unnamed: 0', 'no'], inplace=True)
q.rename(columns={"serialNumber":"StockId"}, inplace=True)

ticker_profile = dict()

for i in p.iterrows():
    print(i[0], i[1][3])
    ticker_profile[i[0]] = i[1][3]

risk_level = {"Conservative":0,
              "Balanced": 1,
              "Assertive":2,
              "Aggressive":3,
              "Very Aggressive": 4}
print(ticker.loc[0, 'symbol'])

def classify(cat, stockid):
    stockId = ticker.loc[stockid-1, 'symbol']
    print(stockId)
    if cat == 'Conservative':
        if stockId in Ticker_Profile['Conservative'] or stockId in Ticker_Profile['Balanced']: # or stockId in Ticker_Profile['Assertive']:
            return True
        else:
            return False
    elif cat == 'Balanced':
        if stockId in Ticker_Profile['Conservative'] or stockId in Ticker_Profile['Assertive'] or stockId in Ticker_Profile['Balanced']: # or stockId in Ticker_Profile['Aggressive']:
            return True
        else:
            return False
    elif cat == 'Assertive':
        if stockId in Ticker_Profile['Balanced'] or stockId in Ticker_Profile['Assertive'] or stockId in Ticker_Profile['Aggressive']: # or stockId in Ticker_Profile['Aggressive'] or stockId in Ticker_Profile['Very Aggressive']:
            return True
        else:
            return False
    elif cat == 'Aggressive':
        if stockId in Ticker_Profile['Aggressive'] or stockId in Ticker_Profile['Assertive'] or stockId in Ticker_Profile['Very Aggressive']: #or stockId in Ticker_Profile['Very Aggressive']:
            return True
        else:
            return False
    else:
        if stockId in Ticker_Profile['Aggressive'] or stockId in Ticker_Profile['Very Aggressive'] :#or stockId in Ticker_Profile['Assertive'] :
            return True
        else:
            return False
        

# Customer Stock List
customer_stock_List = dict()
for i in trans.iterrows():
    custId = i[1][3]
    stockId = i[1][0]
    try:
        if custId in customer_stock_List and stockId not in customer_stock_List[i[1][3]]["stocks"]:
            customer_stock_List[i[1][3]]["stocks"].append(stockId)
            cat = customer_stock_List[custId]["nature"]
            if classify(cat, stockId) is False:
                customer_stock_List[i[1][3]]['outlier'].append(stockId)
        else:
            cat = risk_profile.loc[custId-1,'binned']
            stockId = i[1][0] 
            customer_stock_List[i[1][3]] = {
                    "stocks":[stockId],
                    "nature": cat,
                    "outlier": []
                    }
            if classify(cat, stockId) is False:
                customer_stock_List[i[1][3]]['outlier'].append(stockId)    
    except KeyError:
        break

l_index = list(risk_profile.index.values)
l_index.pop(5180)
print( risk_profile.loc[1,'binned'])
l_index.append(5181)
risk_profile['customerId'] = l_index
# Risk Profile of Customers as dictionary form
    

# Ticker Profile as Dictionary
Ticker_Profile = {
        "Conservative":[],
        "Balanced":[],
        "Assertive":[],
        "Aggressive":[],
        "Very Aggressive":[]
        }
for i in p.iterrows():
    Ticker_Profile[i[1][3]].append(i[1][4])
    
data.columns.values
for i in data.iterrows():
    a = i[1].to_dict()
    break

# for i in customer_stock_List:
    