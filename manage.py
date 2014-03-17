# manage.py
import os

from flask.ext.script import Manager, Shell, Server
from flask.ext.security import MongoEngineUserDatastore
#from flask.ext.security.utils import encrypt_password

from threethings import create_app
from threethings.config import ProductionConfig, DevelopmentConfig
from threethings.extensions import db
from threethings.user import User, Role

if os.environ.get('PRODUCTION'):
    app = create_app(config = ProductionConfig)
else:
    app = create_app()

manager = Manager(app)

@manager.command
def initdb():
    '''Init/reset database.'''
    if not os.environ.get('PRODUCTION'):
        db.connection.drop_database(app.config['MONGODB_DB'])

    user_datastore = MongoEngineUserDatastore(db, User, Role)

    admin_role = user_datastore.create_role(name='admin', description='Admin User')
    user = user_datastore.create_user(
        email='joe.a.hand@gmail.com',
        password='password'
    )

    user_datastore.add_role_to_user(user, admin_role)

@manager.command
def buildjs():
    ''' Builds the js for production
        TODO: Build css here too.
    '''
    jsfile = 'app.min.js'
    os.system('cd 3things/static/js && node libs/r.js -o app.build.js out=../build/%s'%jsfile)
    os.system('cd 3things/static/js && cp libs/require.js ../build/')
    jsfile = '3things/static/build/' + jsfile

def shell_context():
    return dict(app=app)

#runs the app
if __name__ == '__main__':
    manager.add_command('shell', Shell(make_context=shell_context))
    manager.run()
