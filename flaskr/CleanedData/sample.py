#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 10:21:04 2019

@author: hritik
"""
import pandas as pd
import numpy as np
import datetime
import quandl

quandl.ApiConfig.api_key = 'k44yWd6JYdYJ4atkfx64'
Ticker1 = pd.read_csv('ticker.csv')
trans = pd.read_csv('Trans2.csv')
data = pd.read_csv('Stockdata.csv')

# convert ticker dataframe into dictionary
Ticker = Ticker1['symbol']
tick_dict = Ticker
tick = [k for k in tick_dict]

# fetch data using quandl api for list of ticker in the given time range
data = quandl.get_table('WIKI/PRICES', ticker= tick,
                        qopts = {'columns': ['date', 'ticker', 'adj_close']},
                        date = {'gte': '2007-1-1', 'lte': '2016-12-31'}, paginate=True)

# since there is lot of missing data for some required ticker so we are
# replacing those ticker witk similar mean ans veriance value
b = trans
b.drop(columns='Unnamed: 0',inplace=True)
b.drop(columns='no',inplace=True)
b['StockId'].replace(27,86, inplace=True)
b['StockId'].replace(40,76, inplace=True)
b['StockId'].replace(30,87, inplace=True)
b['StockId'].replace(42,79, inplace=True)
b['StockId'].replace(12,67, inplace=True)

# creating stock table for fetched data with datatimeIndex
clean = data.set_index('date')

# pivoting each ticker value with respect to date
stock_table = clean.pivot(columns='ticker')
stock_table.info()
stock_table.describe()
a = stock_table.describe()

# changing index into datetimeIndex
clean_trans = trans.set_index('trans_date')

# pivoting datafrme across StockId column
trans_table = clean_trans.pivot(columns='StockId')

# closing_p being the list to which we will fill closing price of the stocks into the transaction dataframe
closing_p = list()
stock_table[('None','CXO')].fillna(stock_table[('None','CXO')].mean(), inplace=True)
stock_table[('None','V')].fillna(stock_table[('None','V')].mean(), inplace=True)
stock_table.describe()

for rows in trans.iterrows():
    try:
        t_date = rows[1]['trans_date']
        s_id = rows[1]['StockId']
        s_id_ticker = Ticker[s_id-1]
        closing_price = stock_table.loc[t_date]['adj_close',s_id_ticker]
        if closing_price is 'nan':
            break
        closing_p.append(closing_price)
    except KeyError:
        i = 1
        while True:
            try:
                d = (datetime.datetime.strptime('2015-11-26', '%Y-%m-%d').date() + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
                closing_price = stock_table.loc[d]['adj_close',s_id_ticker]
                if closing_price == 'nan':
                    break
        
                closing_p.append(closing_price)
                break
            except KeyError:
                i+=1
                continue
        continue

closing_p.describe()
    
# (datetime.datetime.strptime('2015-11-26', '%Y-%m-%d').date() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

# inserting a new column in the trans dataframe
b['closing_price'] = closing_p

# filling the remaining nan value using forward fil method
b.fillna( method ='ffill', inplace = True)
b.info()
#b.drop(columns='closing', inplace=True)
b.to_csv('FinalStockTransaction.csv')

# creating new column in transaction dataset the monetry value of transaction
b['MonetryValue'] = b['closing_price']*b['tran_amount']
stock_table.Index.get_loc('2015-11-26', method='nearest')
