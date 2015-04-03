from wtforms import Form, TextField, validators, SubmitField

# create a class for the form
class postcode_input(Form):
	postcode = TextField('postcode',[validators.Length(min=3, max=10)])
	submit = SubmitField("Submit")