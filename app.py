from flask import Flask, Blueprint
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import os
from models import *

from api import UserResource, Marshmallow

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
db = SQLAlchemy(app)
ma = Marshmallow(app)

api.add_resource(UserResource, '/users/<user_id>')

if __name__ == '__main__':
    app.run()
