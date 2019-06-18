import datetime

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

import app
from app import db, ma



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    registration_date = app.db.Column(db.Date, default=datetime.datetime.utcnow)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)

    # @validates('phone_number')
    def __init__(self, first_name, last_name, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def __repr__(self):
        return '<id {}>'.format(self.id)


class UserSchema(ma.Schema):
    class Meta:
        # fields = ('first_name', 'last_name', 'registration_date', 'phone_number')
        model = User


user_schema = UserSchema()
users_schema = UserSchema(many=True)
