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
        with requests.Session() as s:
            given(config().session(s)).get('http://www.github.com')
            previous = given(config().session(s).redirects(True)).get('http://www.github.com/staudt/assurest').then().status(equals(200))
            given(config().session(previous.configuration.request_session).redirects(True)).get('http://www.github.com/staudt/assurest').then().status(equals(200))

    def test_redirect(self):
        given().get('http://www.github.com/staudt/assurest').then().status(equals(301))
        given(config().redirects(False)).get('http://www.github.com/staudt/assurest').then().status(equals(301))
        given(config().redirects(True)).get('http://www.github.com/staudt/assurest').then().status(equals(200))


class TestGoogleMaps(unittest.TestCase):
    def setUp(self):
        self.config = config() \
            .base_url('http://maps.googleapis.com') \
            .follow_redirects(True)

    def test_geomap(self):
        given() \
            .config(self.config) \
            .params('address', '1600+Amphitheatre+Parkway,+Mountain+View,+CA',
                    'sensor', 'false') \
            .log('headers') \
            .when() \
                .get('/maps/api/geocode/json') \
            .then() \
                .log('headers') \
                .status(equals(200)) \
                .body(contains('results'))

if __name__ == '__main__':
    unittest.main()