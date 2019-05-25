from .. import db


class User(db.Model):
    __table__name = 'users'
    id = db.Column(db.Integer, primary_key=True)
    holyday = db.Column(db.DateTime, index=True, unique=True, nullable=False)
