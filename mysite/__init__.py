
__author__ = 'ciacicode'
# all the imports

from flask import Flask
from configs.khal_config import Config
import requests
import requests_cache


app = Flask(__name__)
app.config.from_object(Config)
requests_cache.install_cache(cache_name='khaleesi_cache', backend='sqlite', expire_after=180)


import mysite.site_views
import mysite.api
