import json
import unittest
import uuid

import webob

import changeling.fakes
import changeling.wsgi



class TestEmptyService(unittest.TestCase):
    def setUp(self):
        storage = changeling.fakes.FakeStorage([])
        self.app = changeling.wsgi.build_app(storage,
                                             changeling.api.change_api_factory,
                                             changeling.api.auth_api_factory)

    def test_list_changes(self):
        req = webob.Request.blank('/changes')
        resp = req.get_response(self.app)
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], json.loads(resp.body))

    def test_get_unknown_change(self):
        req = webob.Request.blank('/changes/%s' % uuid.uuid4())
        resp = req.get_response(self.app)
        self.assertEqual(404, resp.status_code)

    def test_patch_unknown_change(self):
        req = webob.Request.blank('/changes/%s' % uuid.uuid4(),
                                  method='PATCH', body="[]",
                                  headers={'content-type': 'application/json'})
        resp = req.get_response(self.app)
        self.assertEqual(404, resp.status_code)

    def test_delete_unknown_change(self):
        req = webob.Request.blank('/changes/%s' % uuid.uuid4(),
                                  method='DELETE')
        resp = req.get_response(self.app)
        self.assertEqual(404, resp.status_code)

    def test_get_unknown_change_history(self):
        req = webob.Request.blank('/changes/%s/history' % uuid.uuid4())
        resp = req.get_response(self.app)
        self.assertEqual(404, resp.status_code)


class TestLoadedService(unittest.TestCase):
    def setUp(self):
        self.fixtures = [
            changeling.models.Change(name='ping'),
            changeling.models.Change(name='pong', tags=['foo', 'bar']),
        ]
        storage = changeling.fakes.FakeStorage(self.fixtures)
        self.app = changeling.wsgi.build_app(storage,
                                             changeling.api.change_api_factory,
                                             changeling.api.auth_api_factory)
        self.app.debug = True

    def test_list_changes(self):
        req = webob.Request.blank('/changes')
        resp = req.get_response(self.app)

        self.assertEqual(200, resp.status_code)

        expected = [c['id'] for c in self.fixtures]
        actual = [c['id'] for c in json.loads(resp.body)]
        self.assertEqual(expected, actual)

    def test_get_change(self):
        change_id = self.fixtures[0]['id']
        req = webob.Request.blank('/changes/%s' % change_id)
        resp = req.get_response(self.app)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(change_id, json.loads(resp.body)['id'])

    def test_get_change_history(self):
        url = '/changes/%s/history' % self.fixtures[0]['id']
        req = webob.Request.blank(url)
        resp = req.get_response(self.app)
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], json.loads(resp.body))
