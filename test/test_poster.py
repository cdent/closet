import sys
import os
import re

from wsgi_intercept import httplib2_intercept
import wsgi_intercept
import httplib2

sys.path.append('closet')
from closet import closet

def setup_module(module):
    module.config_dict = closet.config
    from closet import poster
    from closet import putter # need to start this guy up too
# we have to have a function that returns the callable,
# Selector just _is_ the callable
    def poster_fn():
        return poster.urls
    def putter_fn():
        return putter.urls
    #wsgi_intercept.debuglevel = 1
    domain = 'our_test_domain'
    config_dict['poster']['host_url'] = 'http://%s' % domain
    config_dict['poster']['port'] = 8000
    config_dict['putter']['host_url'] = 'http://%s' % domain
    config_dict['putter']['port'] = 8001
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('our_test_domain', 8000, poster_fn) 
    wsgi_intercept.add_wsgi_intercept('our_test_domain', 8001, putter_fn) 

def test_poster():
    http = httplib2.Http()
    response, content = http.request('http://our_test_domain:8000/',
            method='POST',
            body='thats amazing',
            headers={'X-Closet-Cookie': config_dict['public_auth_cookie']})
    desired_url = r'%s:%s/\w+' \
            % (config_dict['getter']['host_url'], config_dict['getter']['port'])
    url_re = re.compile(desired_url)
    assert url_re.match(response['location']), \
           'location response on POST should be like %s, is %s' \
            % (desired_url, response['location'])
    assert response['status'] == '201', 'status should be 201 is %s' \
            % response['status']
# content is not getting filled for some reason so this test is failing
    assert url_re.match(content), 'body content should be url %s, is %s' \
            % (desired_url, content)

