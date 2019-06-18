from flask import request
from flask_restful import Resource

from models import *


class UserResource(Resource):
    def get(self, ):
        users = User.query.all()
        users = users_schema.dump(users).data
        return {'status': 'success', 'data': users}, 200
    #
    # def post(self, args, user_id):
    #     json_data = request.get_json(force=True)
    #     if not json_data:
    #         return {'message': 'No input data provided.'}, 400
    #     data, errors = user_schema.load(json_data)
    #     if errors:
    #         return errors, 422
    #     user = User.query.filter_by(phone_number=data['phone_number']).first()
    #     if user:
    #         return {'message': 'User already exists.'}, 400
    #     user = User(first_name=json_data['first_name'],
    #                 last_name=json_data['last_name'],
    #                 phone_number=json_data['phone_number'])
    #
    #     db.session.add(user)
    #     db.session.commit()
    #
    #     result = user_schema.dump(user).data
    #     return {'status': 'success', 'data': result}, 201
    #
    # def put(self, args, user_id):
    #     json_data = request.get_json(force=True)
    #     if not json_data:
    #         return {'message': 'No input provided.'}, 400
    #
    #     data, errors = user_schema.load(json_data)
    #     if errors:
    #         return {'message': 'User does not exist'}, 404
    #     user = User.query.filter_by(id=data['id']).first()
    #     user.first_name = json_data['first_name']
    #     user.last_name = json_data['last_name'] or None
    #     user.phone_number = json_data['phone_number'] or None
    #     user.registration_date = json_data['registration_date'] or None
    # @use_args(user_args)
    # def delete(self, user_id):
    #     user = User.query.filter_by(id=user_id)
    #     if not user:
    #         return {'message': 'User does not exist.'}, 404
    #     user = User.query.filter_by(id=user_id).delete()
    #     db.session.commit()
    #     return {'status': 'success'}, 204
