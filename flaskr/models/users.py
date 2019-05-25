from .. import db


class User(db.Model):
    __table__name = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=False, unique=True, nullable=False)
    email = db.Column(db.String(64), index=False, unique=True, nullable=False)
    FirstName = db.Column(db.String(64), index=False, unique=True, nullable=False)
    LastName = db.Column(db.String(64), index=True, unique=True, nullable=False)
    created = db.Column(db.DateTime, index=True, unique=True, nullable=False)
    SEX = db.Column(db.Char, index=True, unique=True, nullable=False)
    phone = db.Column(db.Integer, index=True, unique=True, nullable=False)
    Address = db.Column(db.Text, index=True, unique=True, nullable=False)
    city = db.Column(db.String(64), index=True, unique=True, nullable=False)
    state = db.Column(db.String(64), index=True, unique=True, nullable=False)
    postCode = db.Column(db.Integer, index=True, unique=True, nullable=False)
    lat = db.Column(db.Integer, index=True, unique=True, nullable=False)
    lon = db.Column(db.Integer, index=True, unique=True, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)