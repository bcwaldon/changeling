
import unittest

import changeling.api
import changeling.fakes


class TestUnauthenticatedChangeAPI(unittest.TestCase):
    def setUp(self):
        self.fake_storage = changeling.fakes.FakeStorage([])
        self.api = changeling.api.UnauthenticatedChangeAPI(self.fake_storage)

    def test_list_zero_changes(self):
        self.assertEqual([], list(self.api.list()))
