import functools
from flask_cors import CORS, cross_origin
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_pymongo import PyMongo
from flask import current_app, jsonify
from flask_bcrypt import Bcrypt
from flaskr.db import get_db
from datetime import datetime
bp = Blueprint('auth', __name__, url_prefix='/auth')
mongo = PyMongo(current_app)
bcrypt = Bcrypt(current_app)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    user = mongo.db.users
    fname = request.get_json()['firstName']
    lname = request.get_json()['lastName']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    username = request.get_json()['userName']
    created = datetime.utcnow()
    #
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


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        print(request.json)
        print('POST METHOD')
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    if request.method == 'GET':
        print(request.json)
        print('GET METHOD')
    return 'Hello world!! you are in log in part'


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
