from flask.ext.mail import Mail
mail = Mail()

from flask.ext.mongoengine import MongoEngine
db = MongoEngine()

from flask.ext.security import Security
security = Security()
