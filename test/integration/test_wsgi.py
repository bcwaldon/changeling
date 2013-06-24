import unittest

import webob

import changeling.fakes
import changeling.wsgi


class TestWSGI(unittest.TestCase):
    def setUp(self):
        storage = changeling.fakes.FakeStorage([])
        change_api_factory = changeling.api.change_api_factory
        auth_api_factory = changeling.api.auth_api_factory

        self.app = changeling.wsgi.build_app(storage,
                                             change_api_factory,
                                             auth_api_factory)

    def test_list_changes(self):
        req = webob.Request.blank('/changes')
        resp = req.get_response(self.app)
        self.assertEqual(resp.status_code, 200)
