"""
GET a blob from the content store
"""

import selector
import closet

s3 = False
if closet.config.get('aws_access_key'):
    from boto_store import S3Closet
    s3 = S3Closet(closet.config['aws_access_key'], closet.config['aws_secret_key'], closet.config['aws_bucket'])

def getter(environ, start_response):
    """GET request with UUID and return output"""
    uuid = environ['selector.vars']['uuid']
    incoming_etag = environ.get('HTTP_IF_NONE_MATCH')
# the etag and the uuid are the same thing because we are write only
    etag = uuid

    if incoming_etag:
        print "ie: " + incoming_etag
    print "et: " + etag

    if etag == incoming_etag:
        start_response('304 Not Modified', [])
        return []

    f = _read(uuid)
    start_response("200 OK", [('ETag', etag), ('Cache-Control', closet.config['cache_control'])])
    return f

def _read(uuid):
    if s3:
        f = s3.get(uuid)
    else:
        """Read a file from the store given uuid"""
        f = open(closet.config['file_store'] + uuid, 'rb')
    return f

port = closet.config['getter']['port']
urls = selector.Selector()
urls.add('/{uuid}', GET=getter)

