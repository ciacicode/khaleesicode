from flask_wtf import Form
from wtforms import TextField, validators, SubmitField
from wtforms.validators import Required, Length

# create a class for the form
class postcode_input(Form):
	postcode = TextField('postcode', [validators.Required(message=(u"Where is your postcode?")),validators.Length(min=2, max=10)])
	submit = SubmitField('Submit')
