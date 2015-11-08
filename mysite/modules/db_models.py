__author__ = 'ciacicode'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from mysite.configs.khal_config import Config
from flask_wtf import Form
from wtforms import StringField, validators, SubmitField
import re
import translitcodec

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


class Locations(db.Model):
    """
        Defines the columns and keys for Locations table
    """
    id = db.Column(db.Integer, primary_key=True)
    postcode = db.Column(db.String(10))
    area = db.Column(db.String(50))

    def __init__(self, area, postcode):
        self.area = area
        self.postcode = postcode

    def __repr__(self):
        return '%r' % self.area


class FciIndex(db.Model):
    """
        Defines the columns and keys for the Fried Chicken Index Table
    """
    id = db.Column(db.Integer, primary_key=True)
    postcode = db.Column(db.String(10), index=True)
    fci = db.Column(db.Float)
    date = db.Column(db.DateTime)

    def __init__(self, postcode, fci, date=None):
        self.postcode = postcode
        self.fci = fci
        if date is None:
            date = datetime.utcnow()
        self.date = date

    def __repr__(self):
        return 'fci for %r is %f' % (self.postcode, self.fci)


class FciSources(db.Model):
    """
        Defines the columns and keys for the Sources table
    """
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(50))
    last_modified = db.Column(db.DateTime)
    url = db.Column(db.String(255))

    def __init__(self, area, url, last_modified=None):
        self.area = area
        self.url = url
        if last_modified is None:
            last_modified = datetime.utcnow()
        self.last_modified = last_modified

    def __repr__(self):
        return 'Source for %r was last modified on %r' % (self.area, self.last_modified)


class Entries(db.Model):
    """
        Defines the columns and keys for the blog table
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.String(10000))
    slug = db.Column(db.String(300))
    date = db.Column(db.DateTime)
    comments = db.relationship('Comments', backref='entries',
                                lazy='dynamic')
    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.date = datetime.utcnow()
        self.slug = slugify(self.title)



class Comments(db.Model):
    """
        Defines the columns and keys for the comments associated to the entries table
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(600))
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.id'))
    date = db.Column(db.DateTime)
    user_id = db.Column(db.String)

    def __init__(self, text, user_id, entry_id):
        self.text = text
        self.date = datetime.utcnow()
        self.entry_id = entry_id
        self.user_id = user_id


# create a class for the form
class PostcodeInput(Form):
    postcode = StringField('postcode', [validators.DataRequired(message=u"Where is your postcode?"),
                                        validators.Length(min=2, max=10)])
    submit = SubmitField('Submit')


def slugify(text, delim=u'-'):
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = word.encode('translit/long')
        if word:
            result.append(word)
    return unicode(delim.join(result))


def add_blog_post(title, text):
    post = Entries(title,text)
    db.session.add(post)
    db.session.commit()