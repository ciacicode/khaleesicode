__author__ = 'ciacicode'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from mysite.configs.khal_config import Config
from mysite.modules import blog
from flask_wtf import Form
from wtforms import StringField, validators, SubmitField, ValidationError
import re
import translitcodec
from ukpostcodeutils import validation
import json
import pdb
import pycountry

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


class Bottom(db.Model):
    """
        Bottom
    """
    id = db.Column(db.Integer, primary_key=True)
    product_type = db.Column(db.String(4))
    last_updated = db.Column(db.DateTime)
    gender = db.Column(db.String(4))
    category = db.Column(db.String(4))
    waist_hip = db.Column(db.Float())
    brand = db.Columns(db.String(50))
    it = db.Columns(db.Integer())
    uk = db.Columns(db.Integer())
    us = db.Columns(db.Integer())
    waist = db.Columns(db.String())
    hip = db.Columns(db.String())
    numeric = db.Columns(db.Integer)
    std = db.Columns(db.String(10))
    hashkey = db.Columns(db.String(40))

    def __init__(self, product_type, gender,  brand, waist, hip, numeric=None, std=None,  it=None, uk=None, us=None, category=None, last_updated=datetime.utcnow()):
        self.product_type = product_type
        self.gender = gender
        self.brand = brand
        self.waist = waist
        self.hip = hip
        self.numeric = numeric
        self.std = std
        self.it = it
        self.uk = uk
        self.us = us
        self.category = category
        self.last_updated = last_updated
        # get cm waist and hip
        self.waist_hip = float(self.waist['cm'] / self.hip['cm'])
        # generate hash
        self.hashkey = gen_hash()

    def gen_hash(self):
        """
            Generates hash key for a clothing item
        """
        hash_key = product_type + gender + 'w' + self.waist['cm'] + 'h' + self.hip['cm']
        return hash_key


    def __repr__(self):
        return 'Bottom with hashkey %s, brand %s, it size, %d' % (self.hashkey, self.brand, self.it)


class ExternalCall(db.Model):
    """
        Defines the columns that will get us the count of external calls done
        to a specific api
    """
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, index=True)
    response = db.Column(db.String())
    #add id for sharing

    def __init__(self, service, response, timestamp=datetime.utcnow()):
        self.service = service
        # augment a specific entry
        if timestamp is None:
            timestamp = datetime.utcnow()
        self.timestamp = timestamp
        self.response = json.dumps(response)

    def __repr__(self):
        return 'Total calls for %s are %f' % (self.service, self.count)


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
        self.slug = blog.slugify(self.title)



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

    def validate_postcode(form, field):
        """
        Checks the uk postcode is valid
        """
        postcode = field.data
        if validation.is_valid_postcode(postcode):
                pass
        else:
            raise ValidationError('The postcode provided is not a valid uk postcode')


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
    """
    Adds a blogpost to the blogpost database
    """
    post = Entries(title,text)
    db.session.add(post)
    db.session.commit()

def add_call(service, response, timestamp=datetime.utcnow()):
    """
    Adds a call record to the External Call table
    """
    #make sure to pass the sharing id
    call = ExternalCall(service, response, timestamp)
    db.session.add(call)
    #flush to get id
    db.session.flush()
    call_id = call.id
    db.session.commit()
    return call_id

def get_personality(call_id):
    """
    Gets a personality result response by querying the database
    """
    error = "{'error': 'Khaleesicode has no memory of this event.'}'"
    insights_object = ExternalCall.query.filter_by(id = call_id).first()
    if insights_object is None:
        return json.loads(error)
    else:
        personality = insights_object.response
        return json.loads(personality)

def get_total_calls(service, to_date = datetime.utcnow()):
    """
    Gets the total calls done for a service at any given time
    """
    #set defailt total
    total = "Could not find total"
    #get situation right now
    today = date.today()
    from_date = today.replace(day=1) # start of this month
    total = ExternalCall.query.filter(ExternalCall.timestamp <= to_date).filter(ExternalCall.timestamp >= from_date).filter(ExternalCall.service == service).count()
    return total

def clear_external_data():
    meta = db.metadata
    print 'Clear ExternalCall table'
    ExternalCall.query.filter(ExternalCall.service=="watson").delete()
    db.session.commit()
