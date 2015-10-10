
__author__ = 'ciacicode'
# all the imports

from flask import Flask


app = Flask(__name__)
app.config.from_pyfile('/home/maria/Desktop/ciacicode/mysite/mysite/configs/khal_config.cfg')

import mysite.site_views
import mysite.api
