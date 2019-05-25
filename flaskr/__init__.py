import os
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required
from flask_jwt_extended import (create_access_token)
import requests

api_token = 'RW1YDD9JPHV08G67'
api_url_base = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=RW1YDD9JPHV08G67'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.dirname(os.path.dirname(__file__)) + "/static"
template_dir = os.path.dirname(os.path.dirname(__file__)) + "/templates"
# app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config['MONGO_DBNAME'] = 'angularFlask'
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/angularFlask'
    app.config['JWT_SECRET_KEY'] = 'secret'

    mongo = PyMongo(app)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    CORS(app)

    @app.route('/users/register', methods=['POST'])
    def register():
        user = mongo.db.users
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
            'created': created
        })
        print(user_id)
        new_user = user.find_one({'_id': user_id})
        print(new_user)
        print(new_user['email'])
        result = {'email': new_user['email'] + " registered"}

        return jsonify({'result': result})

    @app.route('/users/login', methods=['POST'])
    def login():
        users = mongo.db.users
        email = request.get_json()['email']
        password = request.get_json()['password']
        result = ""
        response = users.find_one({'email': email})
        print(response)
        print(bcrypt.check_password_hash(response['password'], password))
        if response:
            if bcrypt.check_password_hash(response['password'], password):
                print("reached")
                access_token = create_access_token(identity={
                    'firstName': response['firstName'],
                    'lastName': response['lastName'],
                    'email': response['email']
                })
                print("created or not")
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

    if __name__ == '__main__':
        app.run(debug=True)

    return app
