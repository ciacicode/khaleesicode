from flask import Flask, render_template, request, __version__, url_for, session, abort
# importing the class called postcode_input
from fci_form import postcode_input
import os
import config
app = Flask(__name__)
app.debug = True


# Views of the app

@app.route('/')
def index():
  return render_template('layout.html')


@app.route('/fci', methods=['GET', 'POST'])
def fci_form():
	form = postcode_input()
	if request.method == 'POST':
		# handle user input
		postcode = request.form['postcode']
		return 'Form posted for %s' % postcode
	elif request.method == 'GET':
		return render_template('fci_form.html', form = form)


if __name__ == '__main__':
	app.secret_key = config.secret_key
	app.run()