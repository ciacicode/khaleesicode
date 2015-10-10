
__author__ = 'ciacicode'
# all the imports

from flask import Flask
from configs.khal_config import Config


app = Flask(__name__)
app.config.from_object(Config)

import mysite.site_views
import mysite.api
