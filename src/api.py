from flask import Blueprint, request, Response, json
from marshmallow import ValidationError

from src.authentication import Auth
from src.models.usermodel import UserSchema, User

user_api = Blueprint('users', __name__)
user_schema = UserSchema()


@user_api.route('/', methods=['POST'])
def create():
    req_data = request.get_json()
    try:
        data = user_schema.load(req_data)
    except ValidationError as e:
        return custom_response(e.messages, 400)

    user = User.get_a_user_with_phone_number(data.get('phone_number'))

    if user:
        message = {'error': 'User already exists.'}
        return custom_response(message, 400)

    user = User(data)
    user.save()
    ser_data = user_schema.dump(user)
    token = Auth.generate_token(ser_data.get('id'))

    return custom_response({'jwt_token': token}, 201)


@user_api.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    # data, error = user_schema.load(req_data, partial=True)

    try:
        data = user_schema.load(req_data, partial=True)
    except ValidationError as e:
        return custom_response(e.messages, 400)

    if not data.get('phone_number') or not data.get('password'):
        return custom_response({'error': 'Enter your phone number and password.'})

    user = User.get_a_user_with_phone_number(data.get('phone_number'))

    if not user:
        return custom_response({'error': 'Invalid credentials.'}, 400)

    if not user.check_hash(data.get('password')):
        return custom_response({'error': 'Invalid credentials.'}, 400)

    ser_data = user_schema.dump(user)
    token = Auth.generate_token(ser_data.get('id'))

    return custom_response({'jwt_token': token}, 200)


@user_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    users = User.get_all_users()
    ser_users = user_schema.dump(users, many=True)
    ser_users = user_schema.dump(users, many=True)
    return custom_response(ser_users, 200)


@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return custom_response({'error'})


@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
    req_data = request.get_json()
    # data, error = user_schema.load(req_data, partial=True)
    try:
        data = user_schema.load(req_data, partial=True)
    except ValidationError as e:
        return custom_response(e.messages, 400)
    id = Auth.decode_token(request.headers.get('api-token'))['data']['user_id']

    user = User.query.filter_by(id=id).first()
    user.update(data)

    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)


@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
    id = Auth.decode_token(request.headers.get('api-token'))['data']['user_id']

    user = User.query.filter_by(id=id).first()
    user.delete()

    return custom_response({'message': 'Deleted.'}, 204)


@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
    id = Auth.decode_token(request.headers.get('api-token'))['data']['user_id']
    user = User.query.filter_by(id=id).first()
    ser_user = user_schema.dump(user)

    return custom_response(ser_user, 200)


def custom_response(response, status_code):
    return Response(mimetype="application/json", response=json.dumps(response), status=status_code)
