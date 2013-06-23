import unittest
import uuid

import changeling.exception
import changeling.models


class TestChangeModel(unittest.TestCase):
    def test_auto_id(self):
        data = {}
        change = changeling.models.Change(**data)
        self.assertTrue(uuid.UUID(change['id']))

    def test_full_model(self):
        data = {
            'id': '323096f8-d02a-427e-a25a-8f70df27d78b',
            'name': 'foo',
            'description': 'bar',
            'tags': ['ping', 'pong'],
            'wip': True,
            'approved': True,
        }
        change = changeling.models.Change.from_dict(data)

        for key, value in data.items():
            self.assertEqual(value, change[key])

    def test_full_model_to_dict(self):
        data = {
            'id': '323096f8-d02a-427e-a25a-8f70df27d78b',
            'name': 'foo',
            'description': 'bar',
            'tags': ['ping', 'pong'],
            'wip': True,
            'approved': True,
        }

        result = changeling.models.Change(**data).to_dict()

        self.assertEqual(data, result)

    def test_minimal_model(self):
        change = changeling.models.Change.from_dict({})

        self.assertTrue(change['id'] is not None)
        expected = {
            'name': None,
            'description': None,
            'tags': [],
            'wip': False,
            'approved': False,
        }
        for key, value in expected.items():
            self.assertEqual(value, change[key])

    def test_minimal_model_to_dict(self):
        expected = {
            'approved': False,
            'wip': False,
            'tags': [],
        }

        result = changeling.models.Change().to_dict()

        self.assertTrue(result.pop('id') is not None)
        self.assertEqual(expected, result)


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

    #NOTE(bcwaldon): we specifically test id since it is validated by a regex
    def test_change_id(self):
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
