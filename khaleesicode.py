'''
	Flask app for Khaleesicode.com
   	by ciacicode
'''


from flask import Flask, render_template, request, __version__, url_for, session, abort, flash, redirect
# importing the class called postcode_input
from fci_form import postcode_input
import os
import config
import fciUtils
import pdb

#pdb.set_trace()
app = Flask(__name__)
app.debug = True
CSRF_ENABLED = True
SECRET_KEY = config.secret_key
app.secret_key = config.secret_key


# Views of the app

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
        return render_template('fci_form.html',form = form, result = result)
    elif request.method == 'GET':
        return render_template('fci_form.html', form = form)
    else:
        error = 'Enter a valid postcode'
		return render_template('fci_form.html', form=form, error=error)


if __name__ == '__main__':
	app.run(threaded=True)