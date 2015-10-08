__author__ = 'ciacicode'

import sqlite3
from contextlib import closing
import time
from flask import request, session, g, redirect, url_for, abort, render_template
from modules.fci_form import postcode_input
from modules.login_form import login_form
from flask.ext.paginate import Pagination
from modules.charts import *
from flask import jsonify
from modules import db_models
from modules import fciUtils
from khaleesicode import app


# create flask app



# manage db connections for microblog
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('static/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# handling requests
@app.before_request
def before_request():
    g.db = connect_db()
    g.cur = g.db.cursor()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

#views
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/fci', methods=['GET', 'POST'])
def fci_form():
    error = None
    form = postcode_input(request.form)
    if form.validate_on_submit():
        # handle user input
        postcode = request.form['postcode']
        # calculate fci
        result = fciUtils.fci_return(postcode)
        return render_template('fci_form.html', form=form, result=result, map=div, script=script)
    elif request.method == 'GET':
        return render_template('fci_form.html', form=form, map=div, script=script)
    else:
        error = 'Enter a valid postcode'
        return render_template('fci_form.html', form=form, error=error, map=div, script=script)


@app.route('/blog')
def show_entries():
    g.cur.execute('select count(*) from entries')
    total = g.cur.fetchone()[0]
    page, per_page, offset = get_page_items()
    sql = 'select title, text from entries order by date desc limit {}, {}'\
        .format(offset, per_page)
    g.cur.execute(sql)
    entries = [dict(title=row[0], text=row[1]) for row in g.cur.fetchall()]
    pagination = get_pagination(page=page,
                                per_page=per_page,
                                record_name='entries',
                                total=total,
                                format_total=True,
                                format_number=True)
    return render_template('show_entries.html', entries=entries, page=page, per_page=per_page, pagination=pagination)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text, date) values (?, ?, ?)',
                 [request.form['title'], request.form['text'], time.strftime('%Y-%m-%d %H:%M:%S')])
    g.db.commit()
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = login_form(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            username = request.form['username']
            password = request.form['password']
            if username != app.config['USERNAME']:
                error = 'Invalid credentials'
            elif password != app.config['PASSWORD']:
                error = 'Invalid credentials'
            else:
                session['logged_in'] = True
                return redirect(url_for('show_entries'))
    return render_template('login.html', form=form, error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('show_entries'))


# helper functions for pagination
def get_css_framework():
    return app.config['CSS_FRAMEWORK']


def get_link_size():
    return app.config['LINK_SIZE']


def show_single_page_or_not():
    return app.config['SHOW_SINGLE_PAGE']


def get_page_items():
    page = int(request.args.get('page', 1))
    per_page = request.args.get('per_page')
    if not per_page:
        per_page = app.config['PER_PAGE']
    else:
        per_page = int(per_page)

    offset = (page - 1) * per_page
    return page, per_page, offset


def get_pagination(**kwargs):
    kwargs.setdefault('record_name', 'records')
    return Pagination(css_framework=get_css_framework(),
                      link_size=get_link_size(),
                      show_single_page=show_single_page_or_not(),
                      **kwargs
                      )

@app.route('/')
def api_root():
    return "Welcome"


@app.route('/fci')
def api_fci():
    """
    :return: in case of no parameters given it returns the entire mapping of the api endpoints. if a postcode is provided in the form of a gest parameter, it will return the value of the resource
    """
    all_postcodes = postcodes_return()
    all_postcodes = all_postcodes['postcodes']
    if 'postcode' in request.args:
        # check also if the postcode is among the ones we have data for
        p = post_to_area(request.args['postcode'])
        if p in all_postcodes:
            resp = fci_object_return(request.args['postcode'])
            resp = jsonify(resp)
            resp.status_code = 200
            return resp
        else:
            return not_found()
    else:
        resp = jsonify(fci.fci_api_mapping)
        resp.status_code = 200
        return resp


@app.route('/fci/postcodes')
def api_postcodes():
    """

    :return: all the postcodes where there is a Fried Chicken Index value
    """
    fci_api_postcodes = postcodes_return()
    resp = jsonify(fci_api_postcodes)
    resp.status_code = 200
    return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route('/fci/maximum')
def api_maximum():
    """

    :return: the maximum value of fci in the database
    """
    resp = find_max()
    resp = jsonify(resp)
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    app.run(debug=True)