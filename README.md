# Everest
A nice Python library for testing REST services heavily inspired by [Rest Assured](http://rest-assured.io/). It looks like this:

```python
import everest
import everest.matchers

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
It wraps the [requests](http://docs.python-requests.org/en/master/) library to make it possible to perform both the full request and also the validate the response. All in one line of code. You can you the \ character for implicit line continuation (so that you can break lines).
