import json

import boto.s3.connection

import changeling.exception


class S3Storage(object):
    def __init__(self, access, secret, bucket):
        self.access_key = access
        self.secret_key = secret
        self.bucket_name = bucket

        self._connection = None

    def initialize(self):
        #NOTE(bcwaldon): This operation is idempotent
        self.connection.create_bucket(self.bucket_name)

    @property
    def connection(self):
        if self._connection is None:
            self._connection = boto.s3.connection.S3Connection(self.access_key,
                                                               self.secret_key)
        return self._connection

    @property
    def bucket(self):
        return self.connection.get_bucket(self.bucket_name)

    @staticmethod
    def _change_key(change_id):
        return '%s.change' % change_id

    @staticmethod
    def _history_key(change_id):
        return '%s.history' % change_id

    def list_changes(self):
        objects = self.bucket.list()
        for obj in objects:
            if obj.name.endswith('.change'):
                yield json.loads(obj.get_contents_as_string())

    def get_change(self, change_id):
        key = self.bucket.get_key(self._change_key(change_id))
        if key is None:
            raise changeling.exception.ChangeNotFound(change_id)
        return json.loads(key.get_contents_as_string())

    def save_change(self, change_id, change_data):
        key = self.bucket.new_key(self._change_key(change_id))
        key.set_contents_from_string(json.dumps(change_data))

    def delete_change(self, change_id):
        key = self.bucket.get_key(self._change_key(change_id))
        try:
            key.delete()
        except AttributeError:
            raise changeling.exception.ChangeNotFound(change_id)

    def extend_change_history(self, change_id, item_data):
        key = self.bucket.new_key(self._history_key(change_id))
        try:
            key_contents = key.get_contents_as_string()
            history = json.loads(key_contents)
        except boto.exception.S3ResponseError:
            history = []
        history.append(item_data)
        key.set_contents_from_string(json.dumps(history))

    def get_change_history(self, change_id):
        key = self.bucket.get_key(self._history_key(change_id))
        try:
            return json.loads(key.get_contents_as_string())
        except AttributeError:
            return []


def StorageFactory(config):
    obj = S3Storage(config['s3.access_key'],
                    config['s3.secret_key'],
                    config['s3.bucket'])
    obj.initialize()
    return obj
