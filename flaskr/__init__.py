import os
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_jwt_extended import (create_access_token)
import requests
import json
from bson.json_util import dumps
import pymongo
from json import dumps

# from pyramid.arima import auto_arima
from collections import defaultdict
import pandas as pd
import quandl
import random
import numpy as np
import matplotlib.pyplot as plt

api_token = 'RW1YDD9JPHV08G67'
api_url_base = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=RW1YDD9JPHV08G67'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.dirname(os.path.dirname(__file__)) + "/static"
template_dir = os.path.dirname(os.path.dirname(__file__)) + "/templates"



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config['MONGO_DBNAME'] = 'angularFlask'
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/angularFlask'
    app.config['JWT_SECRET_KEY'] = 'secret'

    client = pymongo.MongoClient('mongodb://localhost:27017')
    data = pd.read_csv(BASE_DIR+ '/CleanedData/Stock_table.csv')
    mongo = PyMongo(app)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    CORS(app)

    db = client.angularFlask

    # Collections
    user = db.userDB
    trans = db.transactionsDb
    tick = db.ticker


    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Origin', '*')
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
      return response

    @app.route('/users/register', methods=['POST'])
    def register():
        user = mongo.db.usersDB
        fname = request.get_json()['firstName']
        lname = request.get_json()['lastName']
        email = request.get_json()['email']
        password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
        username = request.get_json()['userName']
        created = datetime.utcnow()

        user_id = user.insert({
            'userName': username,
            'firstName': fname,
            'lastName': lname,
            'email': email,
            'password': password,
            'created': created,
            'CustomerId':user.count()+1
        })
        print(user_id)
        new_user = user.find_one({'_id': user_id})
        print(new_user)
        print(new_user['email'])
        result = {'email': new_user['email'] + " registered"}
        return jsonify({'result': result})

    @app.route('/users/login', methods=['POST'])
    def login():
        print("Hello")
        users = mongo.db.usersDB
        email = request.get_json()['email']
        password = request.get_json()['password']
        result = ""
        response = users.find_one({'email': email})
        print(response)
        print(bcrypt.check_password_hash(response['password'], password))
        if response:
            if bcrypt.check_password_hash(response['password'], password):
                print("reached")
                expires = timedelta(days=1)
                access_token = create_access_token(identity={
                    'CustomerId': response['CustomerId'],
                    'firstName': response['firstName'],
                    'lastName': response['lastName'],
                    'email': response['email']
                },expires_delta=expires)
                print(access_token)
                result = jsonify(access_token=access_token)
            else:
                result = jsonify({'error': "invalid username and password"})
        else:
            result = jsonify({'result': "No result found"})
        return result

    @app.route('/users/data', methods=['GET'])
    @jwt_required
    def fetchData():
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(api_token)
        }
        response = requests.get(api_url_base, headers)
        return response.content.decode('utf-8')

    @app.route('/users/profile', methods=['GET'])
    @jwt_required
    def profileData():
        user = mongo.db.usersDB
        tran = mongo.db.transactionsDb
        current_user = get_jwt_identity()
        tkr = mongo.db.ticker
        # print(current_user)
        userData = user.find_one({'CustomerId': current_user['CustomerId']})
        # userData = json.loads(dumps(userData))
        # print(userData)
        del(userData['_id'])
        trans = tran.find({'customer_id': current_user['CustomerId']})
        transInfo = []
        print(trans)
        for i in trans:
            p = {
                'transactionsId': i['TransactionId'],
                'ticker':tkr.find_one({'serialNumber':i['StockId']})['symbol'],
                'closing_price': i['closing_price'],
                'trans_date': i['trans_date'],
                'monetryValue': i['MonetryValue'],
                'numberOfShare': i['tran_amount'],
                'flag': i['TransactionFlag']
            }
            transInfo.append(p)
        # sorted(lis, key = lambda i: (i['age'], i['name']))
        transInfo = sorted(transInfo, key = lambda i: i['trans_date'])
        return jsonify({'userData':dumps(userData), 'Transactions': dumps(transInfo)})

    @app.route('/users/allocation', methods=['GET'])
    @jwt_required
    def transactions():
        user = mongo.db.usersDB
        userid = request.get_json()['userId']
        transactionsinfo = user.find_one({'CustomerId': userid})
        return jsonify({'tranData': transactionsinfo})

    @app.route('/users/market', methods=['GET'])
    @jwt_required
    def market():
        userid = request.get_json()['userId']
        return jsonify({'tranData': transactionsinfo})


    @app.route('/users/return', methods=['GET'])
    @jwt_required
    def netReturn():
        # Gathring customer data regarding his transactions
        current_user = get_jwt_identity()
        customerId = current_user['CustomerId']
        print(current_user)
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
        # NUE: 60.513037   # NUE_Change: 0.102644   # NUE_Share: 20.000000   # NUE_Return: 0.000000
                table.loc[i[0], mv] = (d[sh]*d[st]) + (d[ch]*LMV) + LMV
                LMV = table.loc[i[0], mv]
        netReturn = 0
        stock_return = {}
        pieSeries = []
        current_stk_val = {}
        print(table)
        for i in symbol_list:
            stock_return[i] = table[i + '_Return'].round(3).to_list()
            pieSeries.append({'symbol':i,'share':stock_return[i][9]})
            current_stk_val[i] = [stock_return[i][9],(table[i+'_Share']*table[i]).sum(),table[i+'_Share'].sum()]
            netReturn += stock_return[i][9]
        print(current_stk_val)
        netReturn = round(netReturn, 3)
        l = table.index.strftime("%Y-%m-%d").tolist()
        return jsonify({'stock_return': stock_return, 'netReturn': netReturn, 'pieSeries':pieSeries})
        
    @app.route('/users/suggestion', methods=['GET', 'POST'])
    @jwt_required
    def getSuggestions():
        # return ""
        current_user = get_jwt_identity()
        customerId = current_user['CustomerId']
        numOfStk = 5

        catOfCust = db.risk_profile.find_one({'CustomerId':customerId})['Classification']
        stockList = db.Ticker_Profile.find_one()[catOfCust]
        
        selected = [db.ticker.find_one({'serialNumber':x})['symbol'] for x in stockList]
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
        port_returns = []
        port_volatility = []
        stock_weights = []
        sharpe_ratio = []
        
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
    
    @app.route('/users/projected', methods=['GET','POST'])
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
    if __name__ == '__main__':
        app.run(debug=True)

    return app
