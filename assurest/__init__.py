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


class TestConfig:
    def __init__(self):
        self.request_follow_redirects = False
        self.default_base_url = None
        self.request_session = None

    def session(self, session):
        if not issubclass(session.__class__, requests.Session):
            raise ValueError('Invalid session type')
        self.request_session = session
        return self

    def follow_redirects(self, follow):
        self.request_follow_redirects = True if follow else False
        return self

    def redirects(self, follow): # just an alias
        return self.follow_redirects(follow)

    def base_url(self, url):
        self.default_base_url = url
        return self

def config():
    return TestConfig()


class TestCase:
    def __init__(self, config=None):
        self.response = None
        self.request = None
        self.config(config)
        self.pre_headers = {}
        self.pre_params = {}

    #Given
    def given(self): #no to be confused with the function given()
        if self.response:
            raise RuntimeError('Can\'t perform pre-request action after the request was performed')
        return self

    def config(self, test_config=None):
        if not test_config:
            self.configuration = config()
        else:
            if not issubclass(test_config.__class__, TestConfig):
                raise ValueError('Config provided is invalid (expected TestConfig class)')
            self.configuration = test_config
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

    def params(self, *params):
        self.given()
        if len(params)<1 or len(params)%2!=0:
            raise ValueError('Headers parameters must be even (name, value, ...)')
        for i in range(0,len(params)-1,2):
            self.pre_params[params[i]] = params[i+1]
        return self

    #When
    def when(self):
        return self.given()

    def perform_request(self, method, url):
        caller = requests.request if not self.configuration.request_session else self.configuration.request_session.request
        if self.configuration.default_base_url and not url.startswith('http'):
            url = self.configuration.default_base_url + url
        self.response = caller(method=method, url=url, headers=self.pre_headers, allow_redirects=self.configuration.request_follow_redirects)
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

    def options(self, url):
        return self.perform_request(method='options', url=url)

    def patch(self, url):
        return self.perform_request(method='patch', url=url)

    def head(self, url):
        return self.perform_request(method='head', url=url)

    def trace(self, url):
        return self.perform_request(method='trace', url=url)

    def then(self):
        if self.response == None:
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
