#! coding:utf-8
"""
app_test.py
http://momijiame.tumblr.com/post/39378516046/python-%E3%81%AE-flask-%E3%81%A7-rest-api-%E3%82%92%E4%BD%9C%E3%81%A3%E3%81%A6%E3%81%BF%E3%82%8B
"""

import json
import unittest

import flask_rest
from fifitools import StatusCodes, ContentType


class FlaskrTestCase(unittest.TestCase):
    """ Flask Test """

    def setUp(self):
        self.app = flask_rest.app.test_client()

    def tearDown(self):
        pass

    def test_helth(self):
        """ test helth check """
        response = self.app.post('/helth')
        self.assertEqual(response.status_code, 200)

    def test_api_get(self):
        """ test api get """

        response = self.app.get('/api/key_is_fifi')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], ContentType.application_json)

    def test_api_get_invalid(self):
        response = self.app.get('/api/noting')
        self.assertEqual(response.status_code, StatusCodes.BadRequest400)


    def test_api_post(self):
        """ test api post """

        content_body = json.dumps({'name': 'baz'}).encode("utf-8")
        assert type(content_body) == bytes

        response = self.app.post('/api/key_is_fifi2',
                                 data=content_body,
                                 content_type=ContentType.application_json)

        self.assertEqual(response.status_code, StatusCodes.created)

    def test_api_post_invalid_content_type(self):
        """ test api post """

        content_body = json.dumps({'name': 'fifi'})
        response = self.app.post('/api/key_is_fifi',
                                 data=content_body,
                                 content_type=ContentType.text_plain) # invalid

        self.assertEqual(response.status_code, StatusCodes.BadRequest400)

    def test_apis(self):
        """test all apis"""

        key = "key_is_apis"
        # post
        content_body_bytes = json.dumps({'name': 'baz'}).encode("utf-8")
        assert type(content_body_bytes) == bytes
        response = self.app.post('/api/'+key,
                                 data=content_body_bytes,
                                 content_type=ContentType.application_json)
        self.assertEqual(response.status_code, StatusCodes.created)

        # get
        response = self.app.get('/api/'+key)
        self.assertEqual(response.status_code, StatusCodes.OK200)
        self.assertEqual(response.headers['Content-Type'], ContentType.application_json)
        content_body_dict = json.loads(response.data.decode("utf-8"))

        # delete
        response = self.app.delete('/api/' + key)
        self.assertEqual(response.status_code, StatusCodes.NoContent)

        # get No Contents
        response = self.app.get('/api/'+key)
        self.assertEqual(response.status_code, StatusCodes.BadRequest400)
        self.assertEqual(response.headers['Content-Type'], ContentType.application_json)
        content_body_dict = json.loads(response.data.decode("utf-8"))

if __name__ == '__main__':
    unittest.main()
