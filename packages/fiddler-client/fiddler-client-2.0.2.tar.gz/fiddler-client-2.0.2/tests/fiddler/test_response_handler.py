import unittest
from unittest import mock

from fiddler.utils.response_handler import JobResponseHandler

try:
    from simplejson import JSONDecodeError
except ImportError:
    from json import JSONDecodeError

from fiddler.exceptions import HttpException
from fiddler.utils.response_handler import BaseResponseHandler


class TestBaseResponseHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.response = mock.MagicMock()

    def test_get_data(self):
        handler = BaseResponseHandler(self.response)
        response_dict = {
            'api_version': '2.0',
            'kind': 'NORMAL',
            'data': {
                'created_at': '2022-06-07T20:35:47.048453+00:00',
                'updated_at': '2022-06-07T20:35:47.048453+00:00',
                'foo': 'bar',
            },
        }
        self.response.json.return_value = response_dict
        resp = handler.get_data()
        self.assertEqual(
            {
                'created_at': '2022-06-07T20:35:47.048453+00:00',
                'updated_at': '2022-06-07T20:35:47.048453+00:00',
                'foo': 'bar',
            },
            resp,
        )

    def test_get_error_details_non_json(self):
        self.response.status_code = 200
        self.response.content = b'This is non json content'
        self.response.json.side_effect = JSONDecodeError('bar', 'foo', 0)
        with self.assertRaises(HttpException):
            _ = BaseResponseHandler(self.response).get_data()


class TestJobResponseHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.response = mock.MagicMock()

    def test_job_response_handler(self):
        uuid = '33cf1de2-1db0-4179-943d-203aebef2633'
        name = 'Ingestion dataset Upload'
        status = 'STARTED'
        progress = 0.0
        error_message = None
        extras = {
            '134bd5f9-6205-44d5-9bbe-b1446fb726c8': {
                'status': 'PENDING',
                'result': {},
                'error_message': None,
            },
            '3b0b5170-ba00-488f-9dd9-128b2595ce5d': {
                'status': 'PANDING',
                'result': {},
                'error_message': None,
            },
        }
        self.response.json.return_value = {
            'data': {
                'uuid': uuid,
                'name': name,
                'status': status,
                'progress': progress,
                'error_message': error_message,
                'extras': extras,
            },
            'api_version': '2.0',
            'kind': 'NORMAL',
        }

        job = JobResponseHandler(self.response)
        self.assertEqual(job.uuid, uuid)
        self.assertEqual(job.name, name)
        self.assertEqual(job.status, status)
        self.assertEqual(job.progress, progress)
        self.assertEqual(job.error_message, error_message)
        self.assertDictEqual(job.extras, extras)


if __name__ == '__main__':
    unittest.main()
