__author__ = 'ciacicode'

from flask import request, session, g, redirect, url_for, abort, render_template, copy_current_request_context
from modules.fci_form import PostcodeInput
from modules.loginform import LoginForm
from modules.db_models import *
from flask_paginate import Pagination
from modules.charts import *
from modules.blog import *
from mysite import app
import pdb
from mysite.configs.khal_config import Config



# # manage db connections for microblog
# def connect_db():
#     return sqlite3.connect(app.config['DATABASE'])
#
#
# def init_db():
#     with closing(connect_db()) as db:
#         with app.open_resource(Config.SQLSCHEMA, mode='r') as f:
#             db.cursor().executescript(f.read())
#         db.commit()
#
#
# handling requests

# @app.before_request
# def before_request():
#     g.db = connect_db()
#     g.cur = g.db.cursor()
#
#
# @app.teardown_request
# def teardown_request(exception):
#     db = getattr(g, 'db', None)
#     if db is not None:
#         db.close()

#views
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/fci', methods=['GET', 'POST'])
def fci_form():
    error = None
    form = PostcodeInput(request.form)
    if form.validate_on_submit():
        # handle user input
        postcode = request.form['postcode']
        # calculate fci
        result = fci.fci_return(postcode)
        return render_template('fci_form.html', form=form, result=result, map=div, script=script)
    elif request.method == 'GET':
        return render_template('fci_form.html', form=form, map=div, script=script)
    else:
        error = 'Enter a valid postcode'
        return render_template('fci_form.html', form=form, error=error, map=div, script=script)


@app.route('/blog')
def show_entries():
    all_entries = db.session.query(Entries)
    all_entries = all_entries.all()
    total = len(all_entries)
    page, per_page, offset = get_page_items()
    # query db for all entries data but start at offset and end at limit per_page
    entries_to_display = db.session.query(Entries).order_by(Entries.date)
    entries = [dict(title=entry.title, text=entry.text) for entry in entries_to_display]
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
    add_blog_post(request.form['title'], request.form['text'])
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
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
