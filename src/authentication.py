import datetime
import os
from functools import wraps

import jwt
from flask import Response, json, request, g

from src.models.usermodel import User


class Auth():
    @staticmethod
    def generate_token(user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), 'HS256').decode('utf-8')

        except Exception as e:
            return Response(
                mimetype='application/type',
                response=json.dumps({'error': 'Error in generating user token.'}),
                status=400
            )

    @staticmethod
    def decode_token(token):
        re = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
            re['data'] = {'user_id': payload['sub']}
            return re
        except jwt.ExpiredSignatureError as e1:
            re['error'] = {'message': 'Tokon expired.'}
            return re
        except jwt.InvalidTokenError as e2:
            re['error'] = {'message': 'Invalid token'}
            return re

    @staticmethod
    def auth_required(func):
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'api-token' not in request.headers:
                return Response(
                    mimetype='application/json',
                    response=json.dumps({'error': 'Authentication token is not available.'}),
                    status=400
                )
            token = request.headers.get('api-token')
            data = Auth.decode_token(token)
            if data['error']:
                return Response(
                    mimetype='application/json',
                    response=json.dump(data['error']),
                    status=400
                )

            user_id = data['data']['user_id']
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return Response(
                    mimetype='application/json',
                    response=json.dumps({'error': 'User does not exist.'}, ),
                    status=400
                )
            g.user = {'id': 'user_id'}
            return func(*args, **kwargs)

        return decorated_auth
