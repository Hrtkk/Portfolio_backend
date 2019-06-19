from .. import db
import datetime
import jwt
from flask import current_app


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=False, unique=True, nullable=False)
    email = db.Column(db.String(64), index=False, unique=True, nullable=False)
    firstName = db.Column(db.String(64), index=False, unique=True, nullable=False)
    fastName = db.Column(db.String(64), index=True, unique=True, nullable=False)
    created = db.Column(db.DateTime, index=True, unique=True, nullable=False)
    sex = db.Column(db.Char, index=True, unique=True, nullable=False)
    phone = db.Column(db.Integer, index=True, unique=True, nullable=False)
    address = db.Column(db.Text, index=True, unique=True, nullable=False)
    city = db.Column(db.String(64), index=True, unique=True, nullable=False)
    state = db.Column(db.String(64), index=True, unique=True, nullable=False)
    postCode = db.Column(db.Integer, index=True, unique=True, nullable=False)
    lat = db.Column(db.Integer, index=True, unique=True, nullable=False)
    lon = db.Column(db.Integer, index=True, unique=True, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __init__(self, email, username, password, firstname, lastname, sex, phone, address, city, state, postcode, lat, lon):
        self.email = email
        self.username = username
        self.password = password
        self.firstName = firstname
        self.lastName = lastname
        self.created = datetime.datetime.now()
        self.sex = sex
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.postCode = postcode
        self.lat = lat
        self.lon = lon


    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :param user_id:
        :return:
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow(),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.confi.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e
@staticmethod
def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer| string
    """
    try:
        payload = jwt.decode(auth_token, current_app.config['SECRET_KEY'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired'
    except jwt.InvalidAlgorithmError:
        return 'Invalid Token'
