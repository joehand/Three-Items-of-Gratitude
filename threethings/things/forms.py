from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.fields import FormField, FieldList
from wtforms.validators import length, optional, required

class ItemForm(Form):
    ''' Form to submit an item of gratitude
    '''
    content = TextField(
                    'What good thing happened?',
                    validators=[required(), length(max=150)]
                )
    details = TextAreaField(
                    'Why did it happen?',
                    validators=[optional()]
                )

class DailyForm(Form):
    ''' Multiple items on one form!! Magic.
    '''
    items = FieldList(FormField(ItemForm), min_entries=3)
