'''
	Flask app for Khaleesicode.com
   	by ciacicode
'''

__author__ = 'ciacicode'
# all the imports

from flask import Flask


app = Flask(__name__)
app.config.from_pyfile('/home/maria/Desktop/ciacicode/khaleesicode/khaleesicode/configs/khal_config.cfg')

import khaleesicode.site_views
import khaleesicode.api
