from .. import db


class User(db.Model):
    __table__name = 'users'
    id = db.Column(db.Integer, primary_key=True)
    Serial = db.Column(db.String(64), index=False, unique=True, nullable=False)
    Number = db.Column(db.String(64), index=False, unique=True, nullable=False)
    tickerSymbol = db.Column(db.String(64), index=False, unique=True, nullable=False)
    Security = db.Column(db.String(64), index=True, unique=True, nullable=False)
