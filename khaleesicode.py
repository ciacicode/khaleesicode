from flask import Flask, render_template, request, __version__, url_for
app = Flask(__name__)
app.debug = True



@app.route('/')
def index():
  return render_template('layout.html')

@app.route('/fci')
def fci_form():
	return render_template('fci_form.html')

if __name__ == '__main__':
  app.run()