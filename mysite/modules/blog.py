__author__ = 'ciacicode'

from mysite.modules.db_models import *
import re



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