import functools
from flask_cors import CORS, cross_origin
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask import jsonify
from flask_jwt_extended import (create_access_token)
from . import db
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from collections import defaultdict
import pandas as pd
import quandl
import random
import numpy as np
import os
import matplotlib.pyplot as plt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data = pd.read_csv(BASE_DIR+'/CleanedData/Stock_table.csv')


bp = Blueprint('allocation', __name__, url_prefix='/')

trans = db.get_db().transactions
tick = db.get_db().ticker

@bp.route('/users/allocation', methods=['GET'])
@jwt_required
def transactions():
    user = db.get_db().users
    userid = request.get_json()['userId']
    transactionsinfo = user.find_one({'CustomerId': userid})
    return jsonify({'tranData': transactionsinfo})

@bp.route('/users/market', methods=['GET'])
@jwt_required
def market():
    userid = request.get_json()['userId']
    return jsonify({'tranData': transactionsinfo})


@bp.route('/users/return', methods=['GET'])
@jwt_required
def netReturn():
    # Gathring customer data regarding his transactions
    current_user = get_jwt_identity()
    customerId = current_user['CustomerId']
    customerId=customerId
    tr = trans.find({'customer_id':customerId})
    stock_trans = list(); symbol_list = []; symbol_dict = {}
    
    for i in tr:
        d = datetime.strptime(i['trans_date'],'%Y-%M-%d')
        stock_trans.append([i['StockId'],i['closing_price'],datetime(d.year, d.month, 1),i['tran_amount']])
        symbol_list.append(tick.find_one({'serialNumber':i['StockId']})['symbol'])
        symbol_dict[i['StockId']] = tick.find_one({'serialNumber':i['StockId']})['symbol']

    symbol_list = list(dict.fromkeys(symbol_list))
    stock_trans.sort(key=lambda x:x[2])
    
    # Gathering historical stock data
    try: 
        data.index = pd.to_datetime(data['date'])
        data.drop(columns=['date'], inplace=True)

    except KeyError:
        pass
    table = data[symbol_list]
    
    # resample date to first of date of each month along with mean of all monthly trasactions
    table = table.resample('AS').mean()
    ret = table.pct_change()
    
    # Inserting table for stock Change and Stock Return 
    for i in ret:
        table[i + '_Change'] = ret[i].to_list()
        table[i + '_Return'] = 0
    
    # for any NaN avalue apply bFill method to fill it
    table.bfill(inplace=True)

    for i in symbol_list:
        table[i + '_Share'] = 0

    for i in stock_trans:
        table.loc[i[2],symbol_dict[i[0]]+'_Share'] += i[3]

    # Calculating Return for each stock
    for stock in symbol_list:
        st = stock
        ch = stock + '_Change'
        sh = stock + '_Share'
        mv = stock + '_Return'
        LMV = 0
        for i in table.iterrows():
            d = i[1].to_dict()
            table.loc[i[0], mv] = (d[sh]*d[st]) + (d[ch]*LMV) + LMV
            LMV = table.loc[i[0], mv]

    netReturn = 0; stock_return = {}; pieSeries = []; current_stk_val = {}

    for i in symbol_list:
        stock_return[i] = table[i + '_Return'].round(3).to_list()
        pieSeries.append({'symbol':i,'share':stock_return[i][9]})
        current_stk_val[i] = [stock_return[i][9],(table[i+'_Share']*table[i]).sum(),table[i+'_Share'].sum()]
        netReturn += stock_return[i][9]
    
    print(current_stk_val)
    netReturn = round(netReturn, 3)
    l = table.index.strftime("%Y-%m-%d").tolist()
    return jsonify({'stock_return': stock_return, 'netReturn': netReturn, 'pieSeries':pieSeries})
    

@bp.route('/users/suggestion', methods=['GET', 'POST'])
@jwt_required
def getSuggestions():
    # return ""
    current_user = get_jwt_identity()
    customerId = current_user['CustomerId']
    numOfStk = 5

    catOfCust = db.get_db().risk_profile.find_one({'CustomerId':customerId})['Classification']
    stockList = db.get_db().ticker_Profile.find_one()[catOfCust]
    
    selected = [db.get_db().ticker.find_one({'serialNumber':x})['symbol'] for x in stockList]
    selected1 = set(selected)

    # Randomly selecting required number of stock from given category of risk stock
    while len(selected1) > numOfStk:
        selected1.remove(random.choice(list(selected1)))
    selected = list(selected1)
    
    # get adjusted closing prices of  selected ticker with Quandl
    quandl.ApiConfig.api_key = 'k44yWd6JYdYJ4atkfx64'
    data = quandl.get_table('WIKI/PRICES', ticker= selected,
                            qopts = {'columns': ['date', 'ticker', 'adj_close']},
                            date = {'gte': '2014-1-1', 'lte': '2016-12-31'}, paginate=True)
    
    clean = data.set_index('date')
    table = clean.pivot(columns='ticker')
    
    # calculate daily and annual returns of the stocks
    returns_daily = table.pct_change()
    returns_annual = returns_daily.mean() * 250
    
    # get daily and covariance of returns of the stock
    cov_daily = returns_daily.cov()
    cov_annual = cov_daily * 250
    
    # empty lists to store returns, volatility and weights of imginary portfolios
    port_returns = []; port_volatility = []; stock_weights = []; sharpe_ratio = []
    
    # set the number of combinations for imaginary portfolios
    num_assets = len(selected)
    num_portfolios = 50000
        
    # set random seed for reproduction's sake
    np.random.seed(101)
    
    # populate the empty lists with each portfolios return, risk and weights
    for single_portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        returns = np.dot(weights, returns_annual)
        volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
        sharpe = returns / volatility
        sharpe_ratio.append(sharpe)
        port_returns.append(returns)
        port_volatility.append(volatility)
        stock_weights.append(weights)
    
    # a dictionary for Returns and Risk value of each Portfolio
    portfolio = {'Returns': port_returns,
                    'Volatility': port_volatility,
                    'Sharpe Ratio': sharpe_ratio}
    
    # extend original dictionary to accomodate each ticker and weight in the portfolio
    for counter, symbol in enumerate(selected):
        portfolio[symbol ] = [weight[counter] for weight in stock_weights]
    
    # make a nice dataframe of the extended dictionary
    df = pd.DataFrame(portfolio)
    
    # get better labels for desired arrangement of columns
    column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock for stock in selected]
    
    # reorder dataframe columns
    df = df[column_order]

    # find min Volatility & max sharp values in the dataframe (df)
    min_volatility = df['Volatility'].min()
    max_sharpe = df['Sharpe Ratio'].max()
    
    # use the min, max values to locate and create the two special portfolios
    sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
    min_variance_port = df.loc[df['Volatility'] == min_volatility]
    
    minVaPo = round((min_variance_port.T)*100,2).to_dict()
    SharpPo = round((sharpe_portfolio.T)*100,2).to_dict()
    
    minVaPo = minVaPo[list(minVaPo.keys())[0]]
    SharpPo = SharpPo[list(SharpPo.keys())[0]]
    
    minVaPo_1 = {}
    sharpe_1 = {}
    
    minVaPo_1['Returns'] = minVaPo['Returns']; minVaPo_1['Sharpe Ratio'] = minVaPo['Sharpe Ratio']; minVaPo_1['Volatility'] = minVaPo['Volatility'] 
    sharpe_1['Returns'] = SharpPo['Returns']; sharpe_1['Sharpe Ratio'] = SharpPo['Sharpe Ratio']; sharpe_1['Volatility'] = SharpPo['Volatility'] 
    del(minVaPo['Returns']); del(minVaPo['Sharpe Ratio']); del(minVaPo['Volatility'])
    del(SharpPo['Volatility']); del(SharpPo['Returns']); del(SharpPo['Sharpe Ratio'])
    
    return jsonify({'SharpPo':SharpPo,'minVaPo':minVaPo, 'SharpPoTicker':sharpe_1,'minVaPoTicker':minVaPo_1})


@bp.route('/users/projected', methods=['GET','POST'])
@jwt_required
def projected_retuen():
    return ""


def forecastedReturn(ticker):
    # data = df.sort_index(ascending=True, axis=0)
    # train = data[:]
    # training = train['Close']
    # model = auto_arima(training, start_p=1, start_q=1,max_p=3, max_q=3, m=12,start_P=0, seasonal=True,d=1, D=1, trace=True,error_action='ignore',suppress_warnings=True)
    # model.fit(training)
    # forecast1 = model.predict(n_periods=60)
    # forecast = pd.DataFrame(forecast1[:],columns=['Prediction'])
    return ""