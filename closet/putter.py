"""
Accept a PUT byte stream and uuid and write content to disk.
"""

import selector
import closet

s3 = False
if closet.config.get('aws_access_key'):
    from boto_store import S3Closet
    s3 = S3Closet(closet.config['aws_access_key'], closet.config['aws_secret_key'], closet.config['aws_bucket'])

@closet.write_access(closet.config['private_auth_cookie'])
def putter(environ, start_response):
    """accept input stream from PUT request and write it at the given uuid"""
    uuid = environ['selector.vars']['uuid'] # wsgi.routing_args coming soon?
    input = environ['wsgi.input']
    length = environ['CONTENT_LENGTH']

    body = _read_input(input, length)
    _write(body, uuid)
    uri = _uri(uuid)

    start_response("204 Updated", [('Location', uri)])

    return [uri]

def _read_input(input, length):
    try:
        length = int(length)
    except ValueError:
        return ''

    return input.read(length)

def _write(body, uuid):
    if s3:
        s3.put(uuid, body)
    else:
        f = open(closet.config['file_store'] + uuid, 'wb')
        f.write(body)
        f.close

def _uri(uuid):
    getter_server = '%s:%s/' % (closet.config['getter']['host_url'], closet.config['getter']['port'])
    return getter_server + uuid

port = closet.config['putter']['port']
urls = selector.Selector()
urls.add('/{uuid}', PUT=putter)
