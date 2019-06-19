import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flask.db import get_db



@bp.route('/users/data', methods=['GET'])
@jwt_required
def fetchData():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {0}'.format(api_token)
    }
    response = requests.get(api_url_base, headers)
    return response.content.decode('utf-8')



@bp.route('/users/profile', methods=['GET'])
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
