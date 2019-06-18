from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models import db
from run import create_app
from app import *
import os

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
