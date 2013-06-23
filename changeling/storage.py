import json

import boto.s3.connection


class Storage(object):
    def __init__(self, config):
        self.config = config
        self._connection = None

    def initialize(self):
        #NOTE(bcwaldon): This operation is idempotent
        self.connection.create_bucket(self.config['s3.bucket'])

    @property
    def connection(self):
        if self._connection is None:
            access = self.config['s3.access_key']
            secret = self.config['s3.secret_key']
            self._connection = boto.s3.connection.S3Connection(access, secret)
        return self._connection

    @property
    def bucket(self):
        return self.connection.get_bucket(self.config['s3.bucket'])

    def list_changes(self):
        objects = self.bucket.list()
        for obj in objects:
            yield json.loads(obj.get_contents_as_string())

    def save_change(self, change_data):
        key = self.bucket.new_key(change_data['id'])
        key.set_contents_from_string(json.dumps(change_data))
