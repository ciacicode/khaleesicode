__author__ = 'ciacicode'

from flask import request, session, g, redirect, url_for, abort, render_template, copy_current_request_context
from modules.fci_form import PostcodeInput
from modules.loginform import LoginForm
from modules.db_models import *
from modules.charts import *
from modules.blog import *
from modules.fci import *
from mysite import app
import pdb
from mysite.configs.khal_config import Config


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
        result = fci_return(postcode)
        return render_template('fci_form.html', form=form, result=result, map=div, script=script)
    elif request.method == 'GET':
        return render_template('fci_form.html', form=form, map=div, script=script)
    else:
        error = 'Enter a valid postcode'
        return render_template('fci_form.html', form=form, error=error, map=div, script=script)


@app.route("/blog/", defaults={'page': 1}, methods=["GET", "POST"])
@app.route("/blog/<int:page>/", methods=["GET", "POST"])
def show_entries(page=1):
    paginated = Entries.query.order_by(Entries.date).paginate(page, app.config['PER_PAGE'], False)
    return render_template('show_entries.html', paginated=paginated)

@app.route("/blog/<slug>")
def show_post(slug):
    entry = Entries.query.filter_by(slug = slug).first_or_404()
    return render_template('entry_detail.html', entry = entry)


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
