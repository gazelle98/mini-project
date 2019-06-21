import os

from flask import Flask

from .api import user_api as user_blueprint
from .config import app_config
from .models import db, bcrypt


def create_app(env_name):
    app = Flask(__name__)
    app.config.from_object(app_config[os.getenv('FLASK_ENV')])
    bcrypt.init_app(app)
    db.app = app
    app.app_context().push()

    db.init_app(app=app)
    app.app_context().push()
    app.register_blueprint(user_blueprint, url_prefix='/api/users')

    @app.route('/', methods=['GET'])
    def index():
        return 'Congratulations! Your first endpoint is workin'

    return app
