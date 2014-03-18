from datetime import datetime, timedelta

from flask import (abort, Blueprint, flash, g, redirect,
                    render_template, request, url_for)

from flask.ext.classy import FlaskView, route
from flask.ext.security import current_user, login_required

from .constants import MESSAGES
from .forms import DailyForm
from .models import Item

things = Blueprint('things', __name__, url_prefix='')

class ItemView(FlaskView):
    ''' Our base View for the main Item
    '''
    route_base = '/'

    def before_request(self, name, **kwargs):
        if current_user.is_active():
            g.items = Item.objects(user_ref=current_user.id)

            if g.items and g.items[0].created_today():
                g.grateful_today = True

    def index(self):
        ''' Our main index view '''
        form = DailyForm(request.form)
        return render_template('index.html', form=form)

    @login_required
    @route('/date/<day>', endpoint='date')
    def get_day(self, day):
        ''' View for a single day'''
        date1 = datetime.strptime(day, '%d-%b-%Y')
        date2 = date1 + timedelta(days=1)

        items = Item.objects(
                    user_ref=current_user.id,
                    created_at__gte=date1,
                    created_at__lt=date2,
                )
        return render_template('single.html', items=items, date = date1)

    @login_required
    def post(self):
        ''' Post route for item '''
        form = DailyForm(request.form)
        if form.validate_on_submit():
            for form_item in form.items:
                item = Item(
                            user_ref=current_user.id,
                            content=form_item.content.data,
                            details=form_item.details.data
                        )
                item.save()
            g.items = Item.objects(user_ref=current_user.id)
            flash(MESSAGES['SUCCESS'])
            form = DailyForm()
            return render_template('index.html', form=form)
        flash(MESSAGES['ERROR_ON_FORM'])
        return render_template('index.html', form=form)

    @login_required
    def put(self, id):
        try:
            return jsonify('PUT ITEM JSON HERE')
        except:
            error = 'Some Error'
            return jsonify({'status':'error', 'error':error}), 400

    @login_required
    def delete(self, id):
        try:
            return jsonify( { 'result': True } )
        except:
            error = 'Some Error'
            return jsonify({'status':'error', 'error':error}), 400

#Register our View Class
ItemView.register(things)
