import sys
import os

from wsgi_intercept import httplib2_intercept
import wsgi_intercept
import httplib2

sys.path.append('.')
from closet import closet

def setup_module(module):
    module.config_dict = closet.config
    from closet.getter import urls
# we have to have a function that returns the callable,
# Selector just _is_ the callable
    def app_fn():
        return urls
    #wsgi_intercept.debuglevel = 1
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('our_test_domain', 8001, app_fn) 

# write in the necessary content
    _write("that's amazing", '123456789')

def _write(content, uuid):
    from closet import putter
    putter._write(content, uuid)

def test_getter_simple():
    http = httplib2.Http()
    response, content = http.request('http://our_test_domain:8001/123456789',
            method='GET')
    assert response['status'] == '200', 'status should be 200 is %s' % response['status']
    assert response['etag'] == '123456789', 'response should include etag 123456789 it is %s' % response['etag']
    assert content == "that's amazing", 'content: %s' % content

def test_getter_etags():
    http = httplib2.Http()
    response, content = http.request('http://our_test_domain:8001/123456789',
            method='GET',
            headers={'If-None-Match': '123456789'})
    assert response['status'] == '304', 'status should be 304 is %s' % response['status']

