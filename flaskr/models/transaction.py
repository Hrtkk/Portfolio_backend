from .. import db


class User(db.Model):
    __table__name = 'users'
    id = db.Column(db.Integer, primary_key=True)
    NumberOfShare = db.Column(db.String(64), index=False, unique=True, nullable=False)
    trasactionDate = db.Column(db.DateTime, index=True, unique=True, nullable=False)
    customerId = db.Column(db.String(64), index=False, unique=True, nullable=False)
    stockId = db.Column(db.String(64), index=False, unique=True, nullable=False)
    transactionFlag = db.Column(db.String(64), index=True, unique=True, nullable=False)
    transactionId = db.Column(db.integer, index=True, unique=True, nullable=False)
