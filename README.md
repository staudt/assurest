# Everest
A nice Python library for testing REST services heavily inspired by [Rest Assured](http://rest-assured.io/).

It looks like this:

```python
from everest import *

given() \
    .header('Accept', 'application/json') \
    .when() \
        .get('http://myserver.com/clients') \
    .then() \
        .status(equals(200)) \
        .body(contains('clientlist')) \
        .response_time(less_than(300))
```

## How it works
It wraps the [requests](http://docs.python-requests.org/en/master/) library to make it possible to perform full HTTP requests along with assertions, all in the same line of code.

Everest assertions are compatible with all Python unit test libraries. How cool is that?
