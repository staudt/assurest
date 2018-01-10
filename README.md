[![PyPI version](https://badge.fury.io/py/assurest.svg)](https://badge.fury.io/py/assurest) [![Build Status](https://travis-ci.org/staudt/assurest.svg?branch=master)](https://travis-ci.org/staudt/assurest)

# Assurest
A nice Python library for testing REST services, inspired by [Rest Assured](http://rest-assured.io/).

It looks like this:

```python
from assurest import *

given() \
    .header('Accept', 'application/json') \
    .when() \
        .get('http://myserver.com/clients') \
    .then() \
        .status(equals(200)) \
        .body(contains('clientlist')) \
        .time(less_than(300))
```
## How it works
It wraps the [requests](http://docs.python-requests.org/en/master/) library to make it possible to perform full HTTP requests along with assertions and configurations, everything in the same line of code.

The built-in assertions will work with any unit test library. How cool is that?

## Why should I consider it?
This library makes for a simple, easy to read format of writing regression tests for REST services. It's a good choice if you're looking for a simple test framework that will be very easy to maintain.

## Using Assurest
### 1. Installation
You need Python 3.x installed. Make sure you have [pip](https://pypi.python.org/pypi/pip) installed and on your path. Then run on your command line:
```
    pip install assurest
```
If pip is not available, try _python -m pip_ instead.

### 2. Using Assurest
Assurest is best paired with a unit test framework (any will work). Pick one and use Assurest as your library to perform requests and assertions.

First, let's import it:
```python
from assurest import *
```
Now you have all of Assurest resources in the same context as your python script. Of couse, you can be more specific than \*, but that is up to you.

The general structure is as follows:
```python
given() \
    # pre-request parameters
    #  i.e. config, headers, session
    .when() \
        # the request itself
        #  i.e. get, post, put
    .then() \
        # post-request validations
```

Now let's perform our first request:
```python
given() \
    .params('address', '1600+Amphitheatre+Parkway,+Mountain+View,+CA',
            'sensor', 'false') \
    .when() \
        .get('http://maps.googleapis.com/maps/api/geocode/json')
    .then() \
        .status(equals(200))
```
This will perform a get call to google maps, that performs a query to the specific address provided in the *params()*, and then will expect a status code 200 in return.

To explain in more detail: **given()** is a factory function that provide the Assurest test class. After *given()*, you enter all pre-request parameters, which can include headers, body content (i.e. parameters, files, form), authentication data, configuration or session information. Then, you have **when()**, which is where you define the action, which is a request method to an URL or path (i.e. get, post, put). After that, **then()** is where the validation and other post-request actions are performed, which include any of the assertions that you can perform.

You might be wondering how these chained methods work. It's quite simple: Every method always returns it's own object, allowing the next method to be called right after it.

Now, because this test passes, it won't give you much of a feedback. If you want to print (or log) details for debugging, you can add the **log()** method anywhere in between methods (put it after then() if you want the response data). This will give you details on everything that was executed. You can also specify the type of data you want with log(**type**), where type can be one of *'all', 'headers', 'body', 'config', 'pre-request', 'request'* or *'response'*.

Of course, you can also break down the test into separate steps like this:
```python
mytest = given()
mytest.params('address', '1600+Amphitheatre+Parkway,+Mountain+View,+CA', 'sensor', 'false')
mytest.get('http://maps.googleapis.com/maps/api/geocode/json') # when() will be automatically called
mytest.status(equals(200))  # then() will also be called automatically
mytest.log('body')
```

You can also set configuration to be able to reuse settings with the **config()** constructor. Like this:
```python
myconfig = config().base_url('http://www.github.com').follow_redirects(True)

given() \
    .config(myconfig) \
    .when() \
        .get('/staudt/assurest') \
    .then() \
        .status(equals(200))
```

## Reference
### given() methods
Factory function for the AssurestTest class. Returns a AssurestTest object.
#### .config(AssurestConfig)
Set a configuration object (which must be AssurestConfig), so that the test will use it's settings.
#### .header(name, value)
Set an individual header for the request.
#### .headers(name, value, [...])
Set an list of headers for the request. Every two parameters is a key and value for the a header.
#### .headers({'name': 'value', [...]})
Same as the previous headers call, but it takes a python dictionary instead.
#### .params(name, value, [...])
Set an list of querystring parameters to be added to the request URL. Every two parameters is a key and value.
#### .params({'name': 'value', [...]})
Same as the previous params call, but takes a python dictionary instead.
#### .session(request_session)
Sets a Requests Session object for the request. This allows you to maintain the session between requests/tests. Please refer to sessions in the [requests](http://docs.python-requests.org/en/master/) library.
### .when() methods
Ends the pre-parameters portion of the test in order to perform a request. It is optional, you can call one of the requests calls below directly.
#### .get(path) / .post(path) / .put(path) / .delete(path) / .patch(path) / .options(path) / .head(path) / .trace(path)
Performs a request according to the name of the method to the specified path (which can be a full URL or continuation of a base_url set in the configuration)
#### .perform_request(method, path)
Performs a requests to an path/URL using a custom method.
### .then() methods
Delimits where the request is performed and the valition of the response starts. This method is optional (it is automatically called by all methods below).
#### .and() / .assert_that()
Optional method for readability, usally used to separate assertions. It doesn't do anything.
#### .status(Matcher)
Assertion for the response status code. Will match status code (i.e **200**) with the Matcher specified in the parameter.
#### .body(Matcher)
Assertion for the response body. Will match body text with the Matcher specified in the parameter.

### config() (class AssurestConfig)
Factory function for the AssurestTest class. Returns a AssurestConfig object.
#### base_url(url)
Set the standard base URL for requests. This base URL will be used when the full URL is not specified in requests with this configuration. For example, if the base URL is *http://www.github.com* and the request path is set to */staudt/assurest*, the request will be to  *http://www.github.com/staudt/assurest*. Default is *None*.
#### session(request_session)
Set the standard requests session for the request. This allows you to maintain the session between requests/tests. Please refer to sessions in the [requests](http://docs.python-requests.org/en/master/) library. Default is *None*.
#### follow_redirects(true_or_false)
Set if the request should automatically follow redirects or not. Default is *False*.
#### redirects(true_or_false)
Same as *follow_redirects*.
#### logger(logger)
Set the logger in which log() message will output to. If none is set, they will be printed to the console.

### Matchers
#### equals(value)
#### one_of(value)
#### contains(value)
#### contains_one_of(value)
