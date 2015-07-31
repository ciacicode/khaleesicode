__author__ = 'ciacicode'
from flask_wtf import Form
from wtforms import TextField, SubmitField


# create a class for the login form
class login_form(Form):
    username = TextField('username')
    password = TextField('password')
    submit = SubmitField('Login')

