__author__ = 'ciacicode'
import os
from mysite import app
import unittest
import pdb

class KhalTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login(app.config['USERNAME'], app.config['PASSWORD'])
        print rv.data
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', app.config['password'])
        assert 'Invalid credentials' in rv.data
        rv = self.login(app.config['USERNAME'], 'defaultx')
        assert 'Invalid credentials'in rv.data

if __name__ == '__main__':
    unittest.main()