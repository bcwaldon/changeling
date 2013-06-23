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
    def test_01_list_empty(self):
        self.assertEqual([], list(self.storage.list_changes()))
