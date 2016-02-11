__author__ = 'ciacicode'
import os
from mysite import app
import unittest
from flask import url_for, session
import pdb

class KhalTests(unittest.TestCase):

    def setUp(self):
        app.config['SECRET_KEY'] = 'sekrit!'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SESSION_COOKIE_DOMAIN'] = None
        self.app = app.test_client()

    def login(self, username, password):
        return self.app.post(url_for('login'), data=dict(
            username=username,
            password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        with app.app_context():
            with app.test_request_context():
                rv = self.login(app.config['USERNAME'], app.config['PASSWORD'])
                assert 'You were logged in' in rv.data
                print 'Login success'
                rv = self.login('wrongusername','wrongpassword')
                assert 'You were logged in' not in rv.data
                print 'Login failure'
                rv = self.login('wrongusername', app.config['PASSWORD'])
                assert 'You were logged in' not in rv.data
                print 'Login failure'
                rv = self.login(app.config['USERNAME'], 'wrongpassword')
                assert 'You were logged in' not in rv.data
                print 'Login failure'
                # test logout
                rv = self.logout()
                assert 'You were logged out' in rv.data
                print 'Logout success'


    def test_api_root(self):
        with app.app_context():
            with app.test_request_context():
                rv = self.app.get('/api')
                assert rv.status_code is 200




if __name__ == '__main__':
    unittest.main()