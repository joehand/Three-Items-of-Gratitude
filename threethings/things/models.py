from datetime import datetime, date

from flask import current_app as app

from .constants import *
from ..extensions import db
from ..user import User
from ..utils import mongo_to_dict

class Item(db.Document):
    user_ref = db.ReferenceField(User)
    content = db.StringField(max_length=150, required=True)
    details = db.StringField()
    created_at = db.DateTimeField(
                default=datetime.utcnow(),
                required=True,
            )

    meta = {
            'ordering': ['-created_at']
            }

    def clean(self):
        '''Clean Data!
           Runs before each save
        '''
        pass

    def to_dict(self):
        return mongo_to_dict(self)

    def created_today(self):
        return self.created_at.date() == date.today()
