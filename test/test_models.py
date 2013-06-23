import unittest
import uuid

import changeling.exception
import changeling.models


class TestChangeModel(unittest.TestCase):
    def test_auto_id(self):
        data = {}
        change = changeling.models.Change(**data)
        self.assertTrue(uuid.UUID(change.id))


class TestChangeModelValidation(unittest.TestCase):
    def _assert_valid(self, data):
        # Check that calling __init__ passes and returns a valid model
        change = changeling.models.Change(**data)
        self.assertTrue(change.is_valid())

        # The fact that from_dict doesn't raise is good enough, but why not
        # explicitly check the validity for fun
        change = changeling.models.Change.from_dict(data)
        self.assertTrue(change.is_valid())

    def _assert_invalid(self, data):
        # Check that calling __init__ passes but returns an invalid model
        change = changeling.models.Change(**data)
        self.assertFalse(change.is_valid())

        # from_dict classmethod will raise when invalid data is provided
        self.assertRaises(changeling.exception.ValidationError,
                          changeling.models.Change.from_dict, data)

    def test_valid_id(self):
        data = [
            {'id': '3ca4a568-3aa8-4998-82ef-30770bd680f2'},
        ]
        [self._assert_valid(d) for d in data]

    def test_invalid_id(self):
        data = [
            {'id': 'foobar'},
            {'id': ''},
        ]
        [self._assert_invalid(d) for d in data]
