__author__ = 'ciacicode'

from flask import request, session, redirect, url_for, abort, render_template, flash
from modules.loginform import LoginForm
from modules.charts import *
from modules.fci import *
from mysite import app
import pdb

#views


@app.route('/', defaults={'page': 1})
def index(page=1):
    paginated = Entries.query.order_by(Entries.date.desc()).paginate(page, app.config['PER_PAGE'], False)
    return render_template('home.html', paginated=paginated)


@app.route('/fci', methods=['GET', 'POST'])
def fci_form():
    error = None
    form = PostcodeInput(request.form)
    script = open_chart()[0]
    div = open_chart()[1]
    if form.validate_on_submit():
        # handle user input
        postcode = str(request.form['postcode'])
        response = fci_object_return(postcode)
        result = response['fci']
        return render_template('fci_form.html', form=form, result=result, map=div, script=script)
    elif request.method == 'GET':
        return render_template('fci_form.html', form=form, map=div, script=script)
    else:
        error = 'Enter a valid postcode'
        return render_template('fci_form.html', form=form, error=error, map=div, script=script)


@app.route("/blog/", defaults={'page': 1}, methods=["GET", "POST"])
@app.route("/blog/<int:page>/", methods=["GET", "POST"])
def show_entries(page=1):
    paginated = Entries.query.order_by(Entries.date.desc()).paginate(page, app.config['PER_PAGE'], False)
    return render_template('show_entries.html', paginated=paginated)


@app.route("/blog/<slug>")
def show_post(slug):
    entry = Entries.query.filter_by(slug=slug).first_or_404()
    return render_template('entry_detail.html', entry=entry)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    add_blog_post(request.form['title'], request.form['text'])
    return redirect(url_for('show_entries'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET','POST'])
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
                flash('You were logged in')
                return redirect(url_for('show_entries'))
    return render_template('login.html', form=form, error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/personality', methods=['GET','POST'])
def personality():
    from modules.personality import Profile, get_personality_insights, generate_data
    error = None
    form = Profile(request.form)
    if form.validate_on_submit():
        # handle user input
        profile_text = (request.form['profile']).encode('utf-8')
        #pass the profile to ibm watson api
        insights = get_personality_insights(profile_text)
        #pass the insights to the chart generating function
        data = generate_data(insights,'needs')
        labels = data['labels']
        raw_scores = data['raw_scores']
        percentiles = data['percentiles']
        return render_template('personality.html', form=form, error=error, labels=labels, raw_scores=raw_scores, percentiles=percentiles)
    elif request.method == 'GET':
        return render_template('personality.html', form=form, error=error)
    else:
        error = 'Enter valid text and not junj'
        return render_template('personality.html', form=form, error=error)
