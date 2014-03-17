from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import length, optional, required

class ItemForm(Form):
    ''' Form to submit an item of gratitude
    '''
    gratitude = TextField(
                    'Gratitude',
                    validators=[required(), length(max=150)]
                )
    details = TextAreaField(
                    'Why?',
                    validators=[optional()]
                )
