import json
import math
import tempfile
import unittest
from http import HTTPStatus
from pathlib import Path
from unittest import mock
from urllib.parse import urljoin

from requests import Response

from fiddler.api.helpers import (
    FILE_NAME_KEY,
    MULTIPART_UPLOAD_KEY,
    RESOURCE_IDENT_KEY,
    UPLOAD_ID_KEY,
    UPLOAD_TYPE_KEY,
    multipart_upload,
    NUM_ROWS_KEY,
    NUM_COLS_KEY,
)
from fiddler.constants import CONTENT_TYPE_OCTET_STREAM_HEADER, UploadType
from tests.fiddler.base import BaseTestCase


class TestFileUpload(BaseTestCase):
    def setUp(self) -> None:
        super(TestFileUpload, self).setUp()
        self.project_name = 'test_project'
        self.file_name = 'foo.csv'
        self.identifier = 'bar'
        self.upload_id = 'foo'
        self.mock_client = mock.MagicMock()
        self.resp = Response()
        self.resp.status_code = HTTPStatus.OK
        base_url = f'datasets/{self._org}:{self.project_name}/'
        self.upload_init_url = urljoin(base_url, 'initialize')
        self.upload_init_resp = json.dumps(
            {
                'data': {'upload_id': self.upload_id, 'file_name': self.file_name},
                'api_version': '2.0',
                'kind': 'NORMAL',
            }
        ).encode('utf-8')
        self.upload_url = urljoin(base_url, 'upload')
        self.upload_complete_url = urljoin(base_url, 'complete')
        self.upload_complete_resp = json.dumps(
            {
                'data': {
                    'status': 'SUCCESS',
                    'file_name': self.file_name,
                    'message': 'Successfully uploaded to blob',
                },
                'api_version': '2.0',
                'kind': 'NORMAL',
            }
        ).encode('utf-8')

    def test_upload_lt_5mb(self):
        upload_type = UploadType.DATASET
        dataset_name = 'ds'
        params = {
            UPLOAD_TYPE_KEY: upload_type,
            MULTIPART_UPLOAD_KEY: False,
            RESOURCE_IDENT_KEY: dataset_name,
            FILE_NAME_KEY: self.file_name,
        }
        self.resp._content = self.upload_init_resp
        self.mock_client.put.return_value = self.resp

        resp = multipart_upload(
            self.mock_client,
            self._org,
            self.project_name,
            dataset_name,
            upload_type,
            Path(__file__)
            .parent.parent.joinpath('datasets', 'data', 'dataset_0.csv')
            .as_posix(),
            self.file_name,
        )

        self.mock_client.put.assert_called_once()
        _, kwargs = self.mock_client.put.call_args
        self.assertEqual(self.upload_url, kwargs.get('url'))
        self.assertDictEqual(params, kwargs.get('params'))
        self.assertDictEqual(CONTENT_TYPE_OCTET_STREAM_HEADER, kwargs.get('headers'))
        self.assertDictEqual(
            resp, {UPLOAD_ID_KEY: self.upload_id, FILE_NAME_KEY: self.file_name}
        )

    def test_upload_gt_5mb(self):
        # creating tempfile > 5MB to trigger multipart upload
        file_size = 6 * 1024 * 1024  # bytes
        chunk_size = 4 * 1024 * 1024  # bytes
        total_chunks = math.ceil(file_size / chunk_size)
        upload_type = UploadType.DATASET
        with tempfile.NamedTemporaryFile(suffix='.csv') as temp_file:
            temp_file.write(b'0' * file_size)

            # step 1: init upload
            upload_init_resp = Response()
            upload_init_resp.status_code = HTTPStatus.OK
            upload_init_resp._content = self.upload_init_resp

            # step 2: Perform chunk upload
            parts = [{'PartNumber': 1, 'ETag': '1'}, {'PartNumber': 2, 'ETag': '2'}]
            upload_chunk_resp = {
                'data': {
                    'status': 'SUCCESS',
                    'message': 'Chunk successfully uploaded',
                    'info': {},
                },
                'api_version': '2.0',
                'kind': 'NORMAL',
            }
            upload_chunk_1_resp = Response()
            upload_chunk_1_resp.status_code = HTTPStatus.OK
            upload_chunk_resp['data'].update({'info': parts[0]})
            upload_chunk_1_resp._content = json.dumps(upload_chunk_resp).encode('utf-8')
            upload_chunk_2_resp = Response()
            upload_chunk_resp['data'].update({'info': parts[1]})
            upload_chunk_2_resp.status_code = HTTPStatus.OK
            upload_chunk_2_resp._content = json.dumps(upload_chunk_resp).encode('utf-8')

            # step 3: complete upload
            upload_complete_resp = Response()
            upload_complete_resp.status_code = HTTPStatus.OK
            upload_complete_resp._content = self.upload_complete_resp

            self.mock_client.post.side_effect = [upload_init_resp, upload_complete_resp]
            self.mock_client.put.side_effect = [
                upload_chunk_1_resp,
                upload_chunk_2_resp,
            ]

            resp = multipart_upload(
                self.mock_client,
                self._org,
                self.project_name,
                self.identifier,
                upload_type,
                temp_file.name,
                self.file_name,
                chunk_size,
            )

        self.assertDictEqual(
            resp,
            {
                'status': 'SUCCESS',
                FILE_NAME_KEY: self.file_name,
                'message': 'Successfully uploaded to blob',
            },
        )

        upload_init_call, upload_complete_call = self.mock_client.post.mock_calls

        _, _, kwargs = upload_init_call
        self.assertEqual(kwargs.get('url'), self.upload_init_url)
        self.assertDictEqual(
            kwargs.get('data'),
            {
                RESOURCE_IDENT_KEY: self.identifier,
                FILE_NAME_KEY: self.file_name,
                UPLOAD_TYPE_KEY: upload_type,
                NUM_ROWS_KEY: 0,
                NUM_COLS_KEY: 1,
            },
        )

        self.assertEqual(
            self.mock_client.put.call_count, total_chunks
        )  # there are 2 chunks uploaded
        _, _, kwargs = self.mock_client.put.mock_calls[0]
        self.assertEqual(kwargs.get('url'), self.upload_url)
        self.assertDictEqual(
            kwargs.get('params'),
            {
                UPLOAD_TYPE_KEY: upload_type,
                MULTIPART_UPLOAD_KEY: True,
                RESOURCE_IDENT_KEY: self.identifier,
                FILE_NAME_KEY: self.file_name,
                UPLOAD_ID_KEY: self.upload_id,
                'part_number': 1,
            },
        )
        self.assertDictEqual(kwargs.get('headers'), CONTENT_TYPE_OCTET_STREAM_HEADER)
        self.assertTrue(kwargs.get('data') is not None)

        _, _, kwargs = upload_complete_call
        self.assertEqual(kwargs.get('url'), self.upload_complete_url)
        self.assertDictEqual(kwargs.get('data'), {'parts': parts})
        self.assertDictEqual(
            kwargs.get('params'),
            {
                UPLOAD_TYPE_KEY: upload_type,
                RESOURCE_IDENT_KEY: self.identifier,
                FILE_NAME_KEY: self.file_name,
                UPLOAD_ID_KEY: self.upload_id,
            },
        )

    def test_upload_file_not_exist(self):
        with self.assertRaises(ValueError):
            multipart_upload(
                self.mock_client,
                self._org,
                self.project_name,
                self.identifier,
                UploadType.DATASET,
                'foo/abc.csv',
                self.file_name,
            )


if __name__ == '__main__':
    unittest.main()
