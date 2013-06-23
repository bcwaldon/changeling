import os

import pytest
import unittest
import uuid

import changeling.config
import changeling.storage


def find_config():
    path = os.environ['CHANGELING_FUNCTIONAL_TEST_CONFIG']
    return changeling.config.load(path)


class Base(object):
    def setUp(self):
        self.config = find_config()
        bucket = 'changeling-testing-%s' % uuid.uuid4()
        self.config['s3.bucket'] = bucket


class TestStorageFactory(Base, unittest.TestCase):
    @pytest.mark.functional
    def test_init(self):
        storage = changeling.storage.StorageFactory(self.config)
        self.assertTrue(isinstance(storage, changeling.storage.S3Storage))


class TestS3Storage(Base, unittest.TestCase):
    def setUp(self):
        super(TestS3Storage, self).setUp()
        self.storage = changeling.storage.StorageFactory(self.config)

    @pytest.mark.functional
    def test_lifecycle(self):
        self.assertEqual([], list(self.storage.list_changes()))

        #NOTE(bcwaldon): Throw an arbitrary property in there to verify
        # that the storage layer isn't doing extra verification
        self.storage.save_change('ding', {'id': 'ding', 'ping': 'pong'})

        self.assertEqual([{'id': 'ding', 'ping': 'pong'}],
                         list(self.storage.list_changes()))
        self.assertEqual({'id': 'ding', 'ping': 'pong'},
                         self.storage.get_change('ding'))

        self.storage.save_change('ding', {'id': 'ding', 'foo': 'bar'})

        self.assertEqual([{'id': 'ding', 'foo': 'bar'}],
                         list(self.storage.list_changes()))
        self.assertEqual({'id': 'ding', 'foo': 'bar'},
                         self.storage.get_change('ding'))

        self.storage.save_change('dong', {'id': 'dong', 'ping': 'pong'})

        expected = [{'id': 'ding', 'foo': 'bar'},
                    {'id': 'dong', 'ping': 'pong'}]
        self.assertEqual(expected, list(self.storage.list_changes()))
        self.assertEqual({'id': 'dong', 'ping': 'pong'},
                         self.storage.get_change('dong'))

        self.storage.delete_change('ding')
        self.assertEqual([{'id': 'dong', 'ping': 'pong'}],
                         list(self.storage.list_changes()))
        self.assertEqual({'id': 'dong', 'ping': 'pong'},
                         self.storage.get_change('dong'))

    def test_not_found(self):
        self.assertRaises(changeling.exception.ChangeNotFound,
                          self.storage.get_change, 'nonexistant')
        self.assertRaises(changeling.exception.ChangeNotFound,
                          self.storage.delete_change, 'nonexistant')

    def test_not_found_after_delete(self):
        self.storage.save_change('deleted', {'id': 'deleted'})
        self.storage.delete_change('deleted')

        self.assertRaises(changeling.exception.ChangeNotFound,
                          self.storage.get_change, 'deleted')
        self.assertRaises(changeling.exception.ChangeNotFound,
                          self.storage.delete_change, 'deleted')
