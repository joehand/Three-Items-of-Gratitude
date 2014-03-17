from datetime import datetime

from .extensions import db

def prettydate(d):
    diff = datetime.utcnow() - d
    s = diff.seconds
    if diff.days > 14 or diff.days < 0:
        return d.strftime('%d %b %y')
    elif diff.days == 1:
        return '1 day ago'
    elif diff.days > 1:
        return '{} days ago'.format(diff.days)
    elif s <= 1:
        return 'just now'
    elif s < 60:
        return '{} seconds ago'.format(s)
    elif s < 120:
        return '1 minute ago'
    elif s < 3600:
        return '{} minutes ago'.format(s/60)
    elif s < 7200:
        return '1 hour ago'
    else:
        return '{} hours ago'.format(s/3600)

def mongo_to_dict(obj):
    return_data = []

    if isinstance(obj, db.DynamicDocument):
        return_data.append(('id',str(obj.id)))
    if isinstance(obj, db.Document):
        return_data.append(('id',str(obj.id)))

    for field_name in obj._fields:

        if field_name in ('id',):
            continue

        data = obj._data[field_name]

        if isinstance(obj._fields[field_name], db.DateTimeField):
            if data:
                return_data.append((field_name, str(data.isoformat())))
        elif isinstance(obj._fields[field_name], db.StringField):
            try:
                data = str(data)
            except:
                data = data
                pass
            return_data.append((field_name, data))
        elif isinstance(obj._fields[field_name], db.FloatField):
            return_data.append((field_name, float(data)))
        elif isinstance(obj._fields[field_name], db.BooleanField):
            return_data.append((field_name, str(data)))
        elif isinstance(obj._fields[field_name], db.IntField):
            return_data.append((field_name, int(data)))
        elif isinstance(obj._fields[field_name], db.ListField):
            return_data.append((field_name, data))
        elif isinstance(obj._fields[field_name],
                db.EmbeddedDocumentField):
            return_data.append((field_name, mongo_to_dict(data)))
        elif isinstance(obj._fields[field_name], db.DictField):
            return_data.append((field_name, data))

    return dict(return_data)
