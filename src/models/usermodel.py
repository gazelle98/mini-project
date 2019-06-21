import datetime
import re

import phonenumbers
from marshmallow import Schema, fields

from . import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    registration_date = db.Column(db.Date, default=datetime.datetime.utcnow)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=True)

    # @validates('phone_number')
    def __init__(self, data):
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.phone_number = data.get('phone_number')
        self.registration_date = datetime.datetime.utcnow().date()
        self.password = self.__generate_hash(data.get('password'))

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password = self.__generate_hash(item)
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_a_user_with_phone_number(phone_number):
        return User.query.filter_by(phone_number=phone_number).first()


def validate_phone_numbers(phone_number):
    pn = phonenumbers.parse(phone_number, None)
    return phonenumbers.is_valid_number(pn)
    # pattern = re.compile("(0/91)?[7-9][0-9]{9}")
    # return pattern.match(phone_number)


class UserSchema(Schema):
    # fields = ('id', 'first_name', 'last_name', 'password', 'phone_number')
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    phone_number = fields.Str(required=True, validate=validate_phone_numbers)
    registration_date = fields.Date(required=False)
