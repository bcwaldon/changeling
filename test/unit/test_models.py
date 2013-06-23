import unittest
import uuid

import changeling.exception
import changeling.models


class TestChangeModel(unittest.TestCase):
    def test_auto_id(self):
        data = {}
        change = changeling.models.Change(**data)
        self.assertTrue(uuid.UUID(change['id']))


class TestChangeModelValidation(unittest.TestCase):
    def _assert_valid(self, data):
        # The lack of a raised exception signals a valid model
        changeling.models.Change(**data)
        changeling.models.Change.from_dict(data)

    def _assert_invalid(self, data):
        # Check that calling __init__ passes but returns an invalid model
        self.assertRaises(changeling.exception.ValidationError,
                          changeling.models.Change, **data)
        self.assertRaises(changeling.exception.ValidationError,
                          changeling.models.Change.from_dict, data)

    def test_valid_id(self):
        data = [
            {'id': '3ca4a568-3aa8-4998-82ef-30770bd680f2'},
        ]
        [self._assert_valid(d) for d in data]

        data = [
            {'id': 'foobar'},
            {'id': ''},
        ]
        [self._assert_invalid(d) for d in data]

    def test_additional_properties_invalid(self):
        self._assert_invalid({'ping': 'pong'})
