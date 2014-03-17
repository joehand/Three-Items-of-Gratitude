from flask import (abort, Blueprint, flash, g, redirect,
                    render_template, request, url_for)

from flask.ext.classy import FlaskView, route
from flask.ext.security import current_user, login_required

from .models import Item
from .forms import ItemForm

things = Blueprint('things', __name__, url_prefix='')

class ItemView(FlaskView):
    ''' Our base View for the main Item
    '''
    route_base = '/'

    def before_request(self, name):
        if current_user.is_active():
            g.items = Item.objects(user_ref=current_user.id)

            if g.items and g.items[0].created_today():
                g.grateful_today = True

    def index(self):
        ''' Our main index view '''
        form = ItemForm(request.form)
        return render_template('index.html', form=form)

    @login_required
    def get(self, id):
        ''' View for a single item'''
        return render_template('index.html')

    @login_required
    def post(self):
        ''' Post route for item '''
        form = ItemForm(request.form)
        if form.validate_on_submit():
            return render_template('index.html', form=form)
        flash('Errors on form')
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
