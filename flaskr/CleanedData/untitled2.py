#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 12:13:24 2019

@author: hritik
"""

import quandl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pyramid.arima import auto_arima
# get adjusted closing prices of 5 selected companies with Quandl
quandl.ApiConfig.api_key = 'k44yWd6JYdYJ4atkfx64'
selected = ['CNP']
data = quandl.get_table('WIKI/PRICES', ticker= selected,
                        qopts = {'columns': ['date', 'ticker', 'adj_close']},
                        date = {'gte': '2016-1-1', 'lte': (datetime.now()+timedelta(-5)).strftime('%Y-%m-%d')}, paginate=True)
data.head()

date = datetime.fromtimestamp(datetime.timestamp(data['date'].max())).date().strftime('%d/%m/%Y')
max_date_from_data = datetime.fromtimestamp(datetime.timestamp(data['date'].max())).date().strftime('%Y-%m-%d')
projection_date = (datetime.fromtimestamp(datetime.timestamp(data['date'].max()))+timedelta(90)).strftime('%Y-%m-%d')
splitter_date = (datetime.fromtimestamp(datetime.timestamp(data['date'].max()))+timedelta(-30)).strftime('%Y-%m-%d')

max_date_from_data, projection_date, splitter_date


data.set_index('date', inplace=True)
data.drop(columns=['ticker'], inplace=True)
data = data.sort_index(ascending=True, axis=0)
training = data[data.index< splitter_date]
test = data[data.index>= splitter_date]


model = auto_arima(training, start_p=1, start_q=1,max_p=3, max_q=3, m=12,start_P=0, seasonal=True,d=1, D=1, trace=True,error_action='ignore',suppress_warnings=True)
model.fit(training)
forecast1 = model.predict(n_periods=60+len(test))

ini_date_range = test.index
a = list(ini_date_range) + list(date_range)
date_range = pd.date_range(start=date,periods=60)
new_data_frame = pd.DataFrame(forecast1,index=a)

current_asset_price = 2000
returns_daily = new_data_frame.pct_change().mean()