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
You need Python 3.x installed. Make sure you have (pip)[https://pypi.python.org/pypi/pip] installed and on your path. Then run on your command line:
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
```
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
This will perform a get call to google maps, that performs a query to the specific address provided in the params(), and then will expect a status code 200 in return.

To explain in more detail: **given()** is a factory function that provide the Asserest test class. After *given()*, you enter all pre-request parameters, which can include headers, body content (i.e. parameters, files, form), authentication data, configuration or session information. Then, you have **when()**, which is where you define the action, which is a request method to an URL or path (i.e. get, post, put). After that, **then()** is where the validation and other post-request actions are performed, which include any of the assertions that you can perform.

You might be wondering how these chained methods work. It's quite simple: After a method performs whatever it is that it does, it will always return it's own object, allowing the next method to be called right after it.
