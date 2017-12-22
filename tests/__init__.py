#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from assurest import *

class TestRequests(unittest.TestCase):
    def setUp(self):
        pass

    def test_simple_request(self):
        given().get('http://www.google.com').then().status(equals(200))

    def test_simple_failure(self):
        with self.assertRaises(AssertionError):
            given().get('http://www.google.com').then().status(equals(201))

    def test_session(self):
        s = requests.Session()
        given(Config(session=s)).get('http://www.github.com')
        previous = given(Config(session=s, redirects=True)).get('http://www.github.com/staudt/assurest').then().status(equals(200))
        given(Config(session=previous.config.session, redirects=True)).get('http://www.github.com/staudt/assurest').then().status(equals(200))

    def test_redirect(self):
        given().get('http://www.github.com/staudt/assurest').then().status(equals(301))
        given(Config(redirects=False)).get('http://www.github.com/staudt/assurest').then().status(equals(301))
        given(Config(redirects=True)).get('http://www.github.com/staudt/assurest').then().status(equals(200))

if __name__ == '__main__':
    unittest.main()