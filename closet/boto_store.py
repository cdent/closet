
from boto.s3.key import Key
from boto.s3.connection import S3Connection

# borrowed from
# http://www.car-chase.net/2007/may/05/simple-database-backups-s3/
# Chase Davis (chase.davis@gmail.com), whom google loves

class S3Closet():
    def __init__(self, access_key, secret_key, bucket_name):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.is_connected = False
        self.bucket = ''

    def connect(self):
        conn = S3Connection(self.access_key, self.secret_key)
        bucket = conn.create_bucket(self.bucket_name)
        self.is_connected = True
        self.bucket = bucket
        return bucket

    def put(self, keyname, data):
        if not self.is_connected:
            self.connect()
        k = Key(self.bucket)
        k.key = keyname
        k.set_contents_from_string(data)

    def get(self, keyname):
        if not self.is_connected:
            self.connect()
        k = Key(self.bucket)
        k.key = keyname
        return k.get_contents_as_string()

