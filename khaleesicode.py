'''
	Flask app for Khaleesicode.com
   	by ciacicode
'''

__author__ = 'ciacicode'
# all the imports
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from fci_form import postcode_input
from login_form import login_form
import config
import fciUtils
import pdb

# configuration


SECRET_KEY = config.secret_key
CSRF_ENABLED = True
DATABASE = config.databaseblog
USERNAME = config.bloguser
PASSWORD = config.blogpass


# create flask app
app = Flask(__name__)
app.debug = True
app.secret_key = config.secret_key
app.config.from_object(__name__)

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
    cur = g.db.execute('select title, text from entries order by id desc')
    #pdb.set_trace()
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = login_form(request.form)
    #pdb.set_trace()
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

if __name__ == '__main__':
	app.run(threaded=True)

