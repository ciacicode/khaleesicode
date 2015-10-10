from flask_wtf import Form
from wtforms import StringField, validators, SubmitField


# create a class for the form
class PostcodeInput(Form):
    postcode = StringField('postcode', [validators.DataRequired(message=u"Where is your postcode?"),
                                        validators.Length(min=2, max=10)])
    submit = SubmitField('Submit')
