__author__ = 'ciacicode'
import os
from mysite import app
import unittest
import json
from flask import url_for
import random as random
from mysite.modules.db_models import Entries
import pdb

class KhalTests(unittest.TestCase):

    def setUp(self):
        app.config['SECRET_KEY'] = 'sekrit!'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SESSION_COOKIE_DOMAIN'] = None
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/maria/Desktop/ciacicode/khaleesicode/mysite/test.db'
        self.app = app.test_client()

    def login(self, username, password):
        return self.app.post(url_for('login'), data=dict(
            username=username,
            password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


    def add_post(self, title, text):
        return self.app.post(url_for('add_entry'), data=dict(
        title=title,
        text=text), follow_redirects=True)

    #test blog login
    def test_login_logout(self):
        with app.app_context():
            with app.test_request_context():
                rv = self.login(app.config['USERNAME'], app.config['PASSWORD'])
                assert 'You were logged in' in rv.data
                rv = self.add_post('Test Title', 'Test Text')
                assert rv.status_code is 200
                rv = self.login('wrongusername','wrongpassword')
                assert 'You were logged in' not in rv.data
                rv = self.login('wrongusername', app.config['PASSWORD'])
                assert 'You were logged in' not in rv.data
                rv = self.login(app.config['USERNAME'], 'wrongpassword')
                assert 'You were logged in' not in rv.data
                # test logout
                rv = self.logout()
                assert 'You were logged out' in rv.data

    #test site pages

    def test_site_views(self):
        with app.app_context():
            with app.test_request_context():
                rv = self.app.get('/')
                assert rv.status_code is 200
                rv = self.app.get('/login')
                assert rv.status_code is 200
                rv = self.app.get('/about')
                assert rv.status_code is 200
                rv = self.app.get('/blog/')
                assert rv.status_code is 200
                assert rv.data is not None
                rv = self.app.get('/fci')
                assert rv.status_code is 200


    # test api endpoints are working
    def test_api_endpoints(self):
        with app.app_context():
            with app.test_request_context():
                rv = self.app.get('/api')
                assert rv.status_code is 200
                rv = self.app.get('/api/fci')
                assert rv.status_code is 200
                rv = self.app.get('/api/fci/postcodes')
                assert rv.status_code is 200
                rv = self.app.get('/api/fci/maximum')
                assert rv.status_code is 200

    #test fci is returned with postcode argument
    def test_api_postcode_arg(self):
        with app.app_context():
            with app.test_request_context():
                #get a postcode from the api
                rv = self.app.get('/api/fci/postcodes')
                res = json.loads(rv.data.decode('utf-8'))
                all_postcodes = res['postcodes']
                ps = random.choice(all_postcodes)
                req_url = '/api/fci?postcode=' + ps
                #test endpoint
                rv = self.app.get(req_url)
                assert rv.status_code is 200
                assert 'fci' in rv.data




if __name__ == '__main__':
    unittest.main()