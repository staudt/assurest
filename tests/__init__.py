#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from assurest import *

class TestAssurest(unittest.TestCase):

    def setUp(self):
        pass

    def test_simple_request(self):
        given().get('http://www.google.com').then().status(equals(200))

    def test_simple_failure(self):
        with self.assertRaises(AssertionError):
            given().get('http://www.google.com').then().status(equals(201))

