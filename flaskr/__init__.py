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
    app.config['JWT_SECRET_KEY'] = 'secret'
    #app.config['DATABASE'] = 'mongodb://hritik:CHINCHI123@cluster0-shard-00-00-gwkzu.gcp.mongodb.net:27017,cluster0-shard-00-01-gwkzu.gcp.mongodb.net:27017,cluster0-shard-00-02-gwkzu.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority'
    client = MongoClient('mongodb://hritik:ZeTtaMiNe@cluster0-shard-00-00-gwkzu.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority')
    data = pd.read_csv(BASE_DIR+ '/CleanedData/Stock_table.csv')
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    CORS(app)
    
    out = client.out
    questions = client.questions
    risk_profile = client.risk_profile
    stock_data = client.stock_data
    ticker = client.ticker
    ticker_profile = client.ticker_profile
    transactions = client.transactions
    users = client.users


    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Origin', '*')
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
      return response

    from . import auth, allocations
    app.register_blueprint(auth.bp)
    app.register_blueprint(allocations.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(market.bp)
    
    if __name__ == '__main__':
        app.run(debug=True)

    return app
