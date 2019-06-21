import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from src.app import create_app, db
from src.models.usermodel import User

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)
migrate = Migrate(app=app, db=db, user=User)

manager = Manager(app=app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
