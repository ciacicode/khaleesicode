'''
	Flask app for Khaleesicode.com
   	by ciacicode
'''

__author__ = 'ciacicode'
# all the imports
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template
from fci_form import postcode_input
from login_form import login_form
import fciUtils
import time
from flask.ext.paginate import Pagination
import pdb




# create flask app
app = Flask(__name__)
app.debug = True
app.config.from_pyfile('khal_config.cfg')

# manage db connections for microblog
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
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
        return render_template('fci_form.html', form=form, result=result)
    elif request.method == 'GET':
        return render_template('fci_form.html', form=form)
    else:
        error = 'Enter a valid postcode'
        return render_template('fci_form.html', form=form, error=error)


@app.route('/blog')
def show_entries():
    #pdb.set_trace()
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

if __name__ == '__main__':
	app.run(port=8000)

