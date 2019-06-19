#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 12:17:59 2019

@author: hritik
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 30 21:26:44 2019

@author: Singhi
"""

import pandas as pd
data = pd.read_csv('sample-orders.csv').drop(columns=['id'])
data['date'] = pd.to_datetime(data['date']).dt.date
data.head()

aaj = pd.to_datetime('31/3/2014').date()

new = pd.DataFrame(columns=['name','recency','frequency','monetary',
                            'r','f','m','RFM class'])
customers = list(set(data['customer']))
new = new.assign(name=customers)
new.set_index('name', inplace=True)
new['recency'] = int(1e10)
new['frequency'] = 0
new['monetary'] = 0

for entry in data.itertuples(index=False):
    name = entry.customer
    new.at[name,'monetary'] += entry.total
    new.at[name,'frequency'] += 1
    if (aaj-entry.date).days<new.at[name,'recency']:
        new.at[name, 'recency'] = (aaj-entry.date).days


new.reset_index(inplace=True)
l = len(new)

new.sort_values('recency', inplace=True)
new.loc[:l//4, 'r'] = 1
new.loc[l//4:l//2, 'r'] = 2
new.loc[l//2:l*3//4, 'r'] = 3
new.loc[l*3//4:, 'r'] = 4

new.sort_values('frequency', inplace=True, ascending=False)
new.loc[:l//4, 'f'] = 1
new.loc[l//4:l//2, 'f'] = 2
new.loc[l//2:l*3//4, 'f'] = 3
new.loc[l*3//4:, 'f'] = 4

new.sort_values('monetary', inplace=True, ascending=False)
new.loc[:l//4, 'm'] = 1
new.loc[l//4:l//2, 'm'] = 2
new.loc[l//2:l*3//4, 'm'] = 3
new.loc[l*3//4:, 'm'] = 4

new['RFM class'] = new.apply(lambda x: f"{x['r']}{x['f']}{x['m']}", axis=1)
new.set_index('name', inplace=True)
new.sort_index(inplace=True)

print(new)