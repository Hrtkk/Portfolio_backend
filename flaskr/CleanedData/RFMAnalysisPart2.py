#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 12:23:21 2019

@author: hritik
"""
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as ply

df = pd.read_csv('Retail_Data_Transactions.csv', parse_dates=['trans_date'])
df.head(3)
# id     customer_id     trans_date           tran_amount
# 0      CS5295          2013-02-11           35
# 1      CS4768          2015-03-15           39
# 2      CS2122          2013-02-26           52


df.info()
# RangeIndex: 125000 entries, 0 to 124999
# Data columns (total 3 columns):
# customer_id    125000 non-null object
# trans_date     125000 non-null datetime64[ns]
# tran_amount    125000 non-null int64
# dtypes: datetime64[ns](1), int64(1), object(1)
# memory usage: 2.9+ MB


print(df['trans_date'].min(), df['trans_date'].max())
# 2011-05-16 00:00:00 2015-03-16 00:00:00

sd = dt.datetime(2015,4,1)
df['hist'] = sd - df['trans_date']
df['hist'].astype('timedelta64[D]')
df['hist'] = df['hist'] / np. timedelta64(1, 'D')
df.head()
# No     customer_id    trans_date          tran_amount    hist
# 0      CS5295         2013-02-11          35            779.0
# 1      CS4768         2015-03-15          39             17.0
# 2      CS2122         2013-02-26          52            764.0
# 3      CS1217         2011-11-16          99           1232.0
# 4      CS1850         2013-11-20          78            497.0

# Only the transactions made in the last 2 years are considered for analysis.

df=df[df['hist'] < 730]
df.info()

rfmTable = df.groupby('customer_id').agg({
                        'hist':         lambda x:x.min(),           # Recency
                        'customer_id':  lambda x: len(x),           # Frequency
                        'tran_amount':  lambda x: x.sum()           # Monetary Value
                        })
rfmTable.rename(columns = {'hist': 'recency',
                           'customer_id': 'frequency',
                           'tran_amount': 'monetary_value'}, inplace = True)

rfmTable.head()
# Cross check the details
df[df['customer_id']=='CS1112']

quartiles = rfmTable.quantile(q=[0.25,0.50,0.75])
print(quartiles, type(quartiles))

quartiles=quartiles.to_dict()
quartiles

## for Recency 

def RClass(x,p,d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]: 
        return 3
    else:
        return 4
    
## for Frequency and Monetary value 

def FMClass(x,p,d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]: 
        return 2
    else:
        return 1    
    
rfmSeg = rfmTable
rfmSeg['R_Quartile'] = rfmSeg['recency'].apply(RClass, args=('recency',quartiles,))
rfmSeg['F_Quartile'] = rfmSeg['frequency'].apply(FMClass, args=('frequency',quartiles,))
rfmSeg['M_Quartile'] = rfmSeg['monetary_value'].apply(FMClass, args=('monetary_value',quartiles,))

rfmSeg['RFMClass'] = rfmSeg.R_Quartile.map(str) \
                            + rfmSeg.F_Quartile.map(str) \
                            + rfmSeg.M_Quartile.map(str)
                            
rfmSeg.head()
rfmSeg.sort_values(by=['RFMClass', 'monetary_value'], ascending=[True, False])

rfmSeg.groupby('RFMClass').agg('monetary_value').mean()

rfmSeg['Total Score'] = rfmSeg['R_Quartile'] + rfmSeg['F_Quartile'] +rfmSeg['M_Quartile']
print(rfmSeg.head(), rfmSeg.info())

rfmSeg.groupby('Total Score').agg('monetary_value').mean()

rfmSeg.groupby('Total Score').agg('monetary_value').mean().plot(kind='bar', colormap='Blues_r')

rfmSeg.groupby('Total Score').agg('frequency').mean().plot(kind='bar', colormap='Blues_r')

rfmSeg.groupby('Total Score').agg('recency').mean().plot(kind='bar', colormap='Blues_r')

res = pd.read_csv('Retail_Data_Response.csv')
res.sort_values('customer_id', inplace=True)

print(res.head(), res.info())

rfmSeg.reset_index(inplace=True)
rfmSeg.head()

rfmSeg.sort_values('customer_id', inplace=True)
rfm2=pd.merge(rfmSeg, res, on='customer_id')

rfm2.info()

ax=rfm2.groupby('Total Score').agg('response').mean().plot(kind='bar', colormap='copper_r')
ax.set_xlabel("Total Score")
ax.set_ylabel("Proportion of Responders")