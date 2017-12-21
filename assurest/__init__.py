import requests
import unittest

class Matcher:
    def __init__(self, expected):
        self.expected = expected

    def __str__(self):
        return "{type} '{val}'".format(type=self.__class__.__name__, val=self.expected)

    def compare_to(self, value):
        return str(self.expected) == value

class equals(Matcher):
    def compare_to(self, value):
        return self.expected == value

class one_of(Matcher):
    def compare_to(self, value):
        for item in expected:
            if self.expected == value:
                return True
        return False

class contains(Matcher):
    def compare_to(self, value):
        return self.expected in value


class Config:
    def __init__(self, session=None, redirects=False):
        self.redirects = redirects
        self.session = None if not session else self.set_session(session)

    def set_session(self, session):
        if not issubclass(session.__class__, requests.Session):
            raise ValueError('Invalid session type')
        self.session = session


class TestCase:
    def __init__(self, config=None):
        self.response = None
        self.request = None
        self.config = config if config else Config()
        self.pre_headers = {}

    #Given
    def given(self): #no to be confused with the function given()
        if self.response:
            raise RuntimeError('Can\'t perform pre-request action after the request was performed')
        return self

    def headers(self, *params):
        #TODO: support dict
        self.given()
        if len(params)<1 or len(params)%2!=0:
            raise ValueError('Headers parameters must be even (name, value, ...)')
        for i in range(0,len(params)-1,2):
            self.pre_headers[params[i]] = params[i+1]
        return self

    def header(self, name, value):
        self.given()
        self.headers(name, value)
        return self

    #When
    def when(self):
        return self.given()

    def perform_request(self, method, url):
        caller = requests.request if not self.config.session else self.config.request
        self.response = caller(method=method, url=url, headers=self.pre_headers, allow_redirects=self.config.redirects)
        self.request = self.response.request
        return self

    def get(self, url):
        return self.perform_request(method='get', url=url)

    def post(self, url):
        return self.perform_request(method='post', url=url)

    def put(self, url):
        return self.perform_request(method='put', url=url)

    def delete(self, url):
        return self.perform_request(method='delete', url=url)

    def then(self):
        if not self.response:
            raise RuntimeError('No request to evaluate (you must perform a request first)')
        return self

    def assertThat(self):
        return self.then()

    def status(self, matcher):
        self.then()
        if not issubclass(matcher.__class__, Matcher):
            raise TypeError('Can only validate with a Matcher type (see matcher types)')
        actual_value = self.response.status_code
        if not matcher.compare_to(actual_value):
            raise AssertionError("Status '{actual}' didn't match expected {expected}".format(actual=actual_value, expected=str(matcher)))
        return self


def given(config=None):
    return TestCase(config)

'''
class AssurestConfig():
    def __init__(self):
        self.follow_redirect = False
        self.base_url = None
'''