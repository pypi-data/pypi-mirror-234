import json
import unittest
from collections import namedtuple
from unittest import mock

from requests import HTTPError

from fiddler.exceptions import (
    ErrorResponseHandler,
    HttpException,
    BadRequest,
)
from fiddler.utils.decorators import handle_api_error_response

try:
    from simplejson import JSONDecodeError
except ImportError:
    from json import JSONDecodeError


class TestErrorResponseHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.http_error = mock.MagicMock()

    def test_get_error_details(self):
        status_code = 409
        message = 'foo'
        errors = [{'reason': 'Conflict', 'message': message, 'help': ''}]
        self.http_error.response.status_code = status_code
        self.http_error.response.json.return_value = {
            'error': {
                'code': status_code,
                'message': message,
                'errors': errors,
            },
            'api_version': '2.0',
            'kind': 'ERROR',
        }
        error_resp_handler = ErrorResponseHandler(self.http_error)
        error_details = error_resp_handler.get_error_details()
        self.assertEqual(error_details.status_code, status_code)
        self.assertEqual(error_details.error_code, status_code)
        self.assertEqual(error_details.message, message)
        self.assertEqual(error_details.errors, errors)

    def test_get_error_details_non_json(self):
        status_code = 409
        error_resp_handler = ErrorResponseHandler(self.http_error)
        self.http_error.response.json.side_effect = JSONDecodeError('bar', 'foo', 1)
        self.http_error.response.status_code = status_code
        with self.assertRaises(HttpException):
            error_details = error_resp_handler.get_error_details()
            self.assertTrue(isinstance(error_details, namedtuple))
            self.assertEqual(error_details.status_code, status_code)


class TestHandleAPIErrorResp(unittest.TestCase):
    @handle_api_error_response
    def raise_http_error(self, status_code: int):
        error_response = {
            'error': {
                'code': status_code,
                'message': '',
                'errors': [],
            },
            'api_version': '2.0',
            'kind': 'ERROR',
        }
        response = mock.MagicMock()
        response.status_code = status_code
        response.content = json.dumps(error_response).encode('utf-8')
        raise HTTPError(response=response)

    def test_wrapper_400(self):
        with self.assertRaises(BadRequest) as ex:  # noqa
            self.raise_http_error(400)

    def test_wraper_happy_path(self):
        @handle_api_error_response
        def foo():
            return True

        self.assertTrue(foo())


if __name__ == '__main__':
    unittest.main()
