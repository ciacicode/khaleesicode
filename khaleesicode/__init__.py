'''
	Flask app for Khaleesicode.com
   	by ciacicode
'''

__author__ = 'ciacicode'
# all the imports

from flask import Flask


app = Flask(__name__)
app.config.from_pyfile('configs/khal_config.cfg')

import khaleesicode.site_views