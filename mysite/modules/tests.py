__author__ = 'ciacicode'
import os
from mysite import app
import unittest
import json
from flask import url_for
import random as random
from db_models import Entries, add_call, get_total_calls, ExternalCall, clear_external_data
from personality import get_personality_insights
from datetime import datetime, timedelta
import pdb

"""
To run this test suit execute the tests.py file from the main khaleesicode directory.
Otherwise the file won't have the context of all the imports.
"""

class KhalTests(unittest.TestCase):

    def setUp(self):
        app.config['SECRET_KEY'] = 'sekrit!'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SESSION_COOKIE_DOMAIN'] = None
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/maria/Desktop/ciacicode/khaleesicode/mysite/khaleesi.db'
        self.app = app.test_client()
        print "Initiating Tests..."

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
                print "Testing login... "
                assert 'You were logged in' in rv.data, "Failed to login"
                rv = self.add_post('Test Title', 'Test Text')
                print "Testing adding a post"
                assert rv.status_code is 200, "Failed add post"
                rv = self.login('wrongusername','wrongpassword')
                print "Testing with wrong username and password"
                assert 'You were logged in' not in rv.data, "Failed: Accepted wrong credentials"
                rv = self.login('wrongusername', app.config['PASSWORD'])
                print "Testing with wrong username only"
                assert 'You were logged in' not in rv.data, "Failed: Accepted wrong username"
                rv = self.login(app.config['USERNAME'], 'wrongpassword')
                print "Testing with wrong password"
                assert 'You were logged in' not in rv.data, "Failed: Accepted wrong password"
                # test logout
                print "Testing Logout"
                rv = self.logout()
                assert 'You were logged out' in rv.data, "Failed to logout"

    #test site pages

    def test_site_views(self):
        with app.app_context():
            with app.test_request_context():
                print "Testing home page"
                rv = self.app.get('/')
                assert rv.status_code is 200, "Failed homepage load"
                print "Testing login page"
                rv = self.app.get('/login')
                assert rv.status_code is 200, "Failed login load"
                print "Testing about page"
                rv = self.app.get('/about')
                assert rv.status_code is 200, "Failed about load"
                print "Testing blog page"
                rv = self.app.get('/blog/')
                assert rv.status_code is 200, "Failed blog load"
                assert rv.data is not None, "Nothing to display"
                print "Testing fci page"
                rv = self.app.get('/fci')
                assert rv.status_code is 200, "Failed fci load"
                print "Testing personality page"
                rv = self.app.get('/personality')
                assert rv.status_code is 200, "Failed personality load"

    # test api endpoints are working
    def test_api_endpoints(self):
        with app.app_context():
            with app.test_request_context():
                print "Testing FCI API"
                rv = self.app.get('/api')
                assert rv.status_code is 200, "Failed: /api is" + str(rv.status_code)
                print "Testing /fci"
                rv = self.app.get('/api/fci')
                assert rv.status_code is 200, "Failed: /api/fci is" + str(rv.status_code)
                print "Testing /postcodes"
                rv = self.app.get('/api/fci/postcodes')
                assert rv.status_code is 200, "Failed: /api/fci/postcodes is" + str(rv.status_code)
                print "Testing /maximum"
                rv = self.app.get('/api/fci/maximum')
                assert rv.status_code is 200, "Failed: /api/fci/maximum" + str(rv.status_code)

    #test fci is returned with postcode argument
    def test_api_postcode_arg(self):
        with app.app_context():
            with app.test_request_context():
                #get a postcode from the api
                print "Testing postcode functions"
                rv = self.app.get('/api/fci/postcodes')
                res = json.loads(rv.data.decode('utf-8'))
                all_postcodes = res['postcodes']
                ps = random.choice(all_postcodes)
                req_url = '/api/fci?postcode=' + ps
                #test endpoint
                rv = self.app.get(req_url)
                assert rv.status_code is 200, "Failed: did not return data for /postcode"
                assert 'fci' in rv.data, "Failed: did not return fci data for valid postcode"


    #test get_personality_insights does not make call if we reached api limit
    def test_watson_call_check(self):
        #fill database with 1000 service calls
        with app.app_context():
            #fill database
            fake_resp = {'response': 'this is a test response'}
            start_timestamp = datetime(2017,07,3,10,20,22)
            print "Filling test database with many service calls"
            for delta in range (0, 1000):
                new_timestamp = start_timestamp + timedelta(minutes=3)
                add_call('watson',fake_resp, timestamp=new_timestamp)
            print "Testing that call limit is enforced"
            ins = get_personality_insights(profile)
            print ins
            assert 'Error message' in ins, "Failed: call limit is not enforced"
        #clear the test table now
        clear_external_data()




if __name__ == '__main__':
    unittest.main()
