
import unittest

import changeling.api
import changeling.fakes


class TestChangeAPI(unittest.TestCase):
    def setUp(self):
        self.fake_storage = changeling.fakes.FakeStorage([])
        self.api = changeling.api.ChangeAPI(self.fake_storage)

    def test_list_zero_changes(self):
        self.assertEqual([], list(self.api.list()))
