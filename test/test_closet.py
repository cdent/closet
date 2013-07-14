
import sys
import os

sys.path.append('.')
from closet import closet

def setup_module(module):
    module.configfile = 'test/closet.yaml'
    module.config_dict = closet.get_config(configfile)
    module.environ = os.environ

def test_simple_config():
    assert config_dict['file_store'] == 'storage/', 'file_store should be storage/'
    assert config_dict['host_url'] == 'http://0.0.0.0', 'host_url should be localhost'

def test_nested_config():
    assert config_dict['poster']['port'] == 8000, 'poster port should be 8000'
    assert config_dict['poster']['host_url'] == 'http://0.0.0.0', 'host_url should be localhost'

def test__write_access():
    environ['HTTP_X_CLOSET_COOKIE'] = config_dict['public_auth_cookie']
    assert closet._write_access(config_dict['public_auth_cookie'], environ), \
            'write access when cookie correct'
    environ['HTTP_X_CLOSET_COOKIE'] = 'bad cookie'
    assert not closet._write_access(config_dict['public_auth_cookie'], environ), \
            'write access fail when cookie bad'
    del environ['HTTP_X_CLOSET_COOKIE']
    assert not closet._write_access(config_dict['public_auth_cookie'], environ), \
            'write access fail when cookie not present' 
    
