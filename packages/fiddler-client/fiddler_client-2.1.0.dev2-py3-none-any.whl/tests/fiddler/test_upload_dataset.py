import unittest
from copy import deepcopy
from http import HTTPStatus
from pathlib import Path
from unittest import mock

import pandas as pd

from fiddler.constants import FileType, UploadType
from fiddler.exceptions import HttpException
from fiddler.schema.dataset import DatasetInfo
from fiddler.schema.server_info import ServerInfo
from tests.fiddler.base import BaseTestCase


class TestUploadDataset(BaseTestCase):
    def setUp(self) -> None:
        super(TestUploadDataset, self).setUp()
        self._project_name = 'test_project'
        self._dataset_name = 'test_dataset'
        self._job_uuid = '3fa85f64-5717-4562-b3fc-2c963f66afa6'
        self._jobs_url = f'{self._url}/jobs/{self._job_uuid}'
        self._job_response = {
            'data': {
                'uuid': self._job_uuid,
                'name': 'Ingestion dataset Upload',
                'status': 'SUCCESS',
                'progress': 100.0,
                'error_message': None,
                'extras': {},
            },
            'api_version': '2.0',
            'kind': 'NORMAL',
        }
        self._datasets_path = Path(__file__).parent.parent.joinpath('datasets', 'data')
        self._data_path = self._datasets_path.joinpath('dataset_0.csv')
        self._info = DatasetInfo.from_dict(
            {
                'name': 'some_name',
                'columns': [
                    {
                        'column-name': 'col0',
                        'data-type': 'int',
                        'value-range-min': 0,
                        'value-range-max': 1,
                        'is-nullable': False,
                    },
                    {
                        'column-name': 'col1',
                        'data-type': 'category',
                        'possible-values': [
                            'hello',
                            'foo',
                        ],
                        'is-nullable': False,
                    },
                    {
                        'column-name': 'col2',
                        'data-type': 'category',
                        'possible-values': [
                            'world',
                            'bar',
                        ],
                        'is-nullable': False,
                    },
                    {
                        'column-name': 'col3',
                        'data-type': 'category',
                        'possible-values': [
                            'True',
                            'False',
                        ],
                        'is-nullable': False,
                    },
                ],
            }
        )
        self.multipart_upload_patcher = mock.patch(
            'fiddler.api.dataset_mixin.multipart_upload'
        ).start()
        self.multipart_upload_patcher.return_value = {
            'status': 'SUCCESS',
            'file_name': 'dataset.csv',
            'message': 'Successfully uploaded to blob',
        }
        self._ingest_url = f'{self._url}/datasets/{self._org}:{self._project_name}:{self._dataset_name}/ingest'
        self._ingest_resp = {
            'data': {
                'status': HTTPStatus.ACCEPTED,
                'job_uuid': self._job_uuid,
                'files': [],
                'message': 'Successfully received the baseline data. Please allow time for the dataset ingestion to complete in the Fiddler platform.',
            },
            'api_version': '2.0',
            'kind': 'NORMAL',
        }
        self._get_project_url = f'{self._url}/projects/{self._org}:{self._project_name}'
        self._get_project_resp = {}

    def test_upload_dataset(self):
        self.requests_mock.get(self._jobs_url, json=self._job_response)
        self.requests_mock.post(
            url=self._ingest_url, json=self._ingest_resp, status=HTTPStatus.ACCEPTED
        )
        files = {
            'train': self._data_path,
            'test': self._data_path,
        }
        output = self.client.upload_dataset_from_file(
            project_id=self._project_name,
            dataset_id=self._dataset_name,
            files=files,
            info=self._info,
        )
        self.assertDictEqual(
            output,
            {
                'uuid': self._job_uuid,
                'name': 'Ingestion dataset Upload',
                'status': 'SUCCESS',
                'progress': 100.0,
                'error_message': None,
            },
        )

        self.assertEqual(
            self.multipart_upload_patcher.call_count, 2
        )  # because we have 2 files
        self.multipart_upload_patcher.assert_called_with(
            client=mock.ANY,
            organization_name=self._org,
            project_name=self._project_name,
            identifier=self._dataset_name,
            upload_type=UploadType.DATASET,
            file_path=str(self._data_path),
            file_name='dataset_0.csv',
        )

    def test_upload_dataset_info_None(self):
        with self.assertRaises(ValueError) as e:  # noqa
            self.client.upload_dataset_from_file(
                project_id=self._project_name,
                dataset_id=self._dataset_name,
                files={
                    'train': self._data_path,
                    'test': self._data_path,
                },
                info=None,
            )

    def test_upload_dataset_info_str(self):
        with self.assertRaises(ValueError) as e:  # noqa
            self.client.upload_dataset_from_file(
                self._project_name,
                self._dataset_name,
                files={
                    'train': self._data_path,
                    'test': self._data_path,
                },
                info='incorrect dataset_info',
            )

    def test_upload_dataset_exception(self):
        self.requests_mock.post(
            url=self._ingest_url, body='some error', status=HTTPStatus.OK
        )
        with self.assertRaises(HttpException) as e:  # noqa
            self.client.upload_dataset_from_file(
                project_id=self._project_name,
                dataset_id=self._dataset_name,
                files={
                    'train': self._data_path,
                    'test': self._data_path,
                },
                info=self._info,
            )

    def test_dataset_empty_file_path_dict(self):
        with self.assertRaises(ValueError) as e:  # noqa
            self.client.upload_dataset_from_file(
                self._project_name, self._dataset_name, {}, {}
            )

    def test_upload_dataset_df(self):
        self.requests_mock.get(
            url=self._get_project_url, json=self._get_project_resp, status=HTTPStatus.OK
        )
        upload_dataset_patcher = mock.patch(
            'fiddler.api.dataset_mixin.DatasetMixin.upload_dataset_from_file'
        ).start()
        response = {
            'uuid': self._job_uuid,
            'name': 'Ingestion dataset Upload',
            'status': 'SUCCESS',
            'progress': 100.0,
            'error_message': None,
        }
        upload_dataset_patcher.return_value = response
        output = self.client.upload_dataset(
            project_id=self._project_name,
            dataset_id=self._dataset_name,
            dataset={
                'train': pd.read_csv(self._data_path),
                'test': pd.read_csv(self._data_path),
            },
            info=self._info,
            is_sync=True,
        )
        self.assertDictEqual(output, response)
        upload_dataset_patcher.assert_called_once_with(
            project_id=self._project_name,
            dataset_id=self._dataset_name,
            files=mock.ANY,  # since we're writing in temp file
            info=self._info,
            file_type=FileType.CSV,
            is_sync=True,
        )
        _, kwargs = upload_dataset_patcher.call_args
        files = kwargs.get('files')
        self.assertListEqual(['train', 'test'], list(files.keys()))
        self.assertEqual(files['train'].name, 'train.csv')

    def test_upload_dataset_df_23_4(self):
        self.requests_mock.get(
            url=self._get_project_url, json=self._get_project_resp, status=HTTPStatus.OK
        )
        upload_dataset_patcher = mock.patch(
            'fiddler.api.dataset_mixin.DatasetMixin.upload_dataset_from_file'
        ).start()
        response = {
            'uuid': self._job_uuid,
            'name': 'Ingestion dataset Upload',
            'status': 'SUCCESS',
            'progress': 100.0,
            'error_message': None,
        }
        upload_dataset_patcher.return_value = response
        server_info = ServerInfo(**{'feature_flags': {}, 'server_version': '23.4.0'})
        with mock.patch.object(
            self.client, 'server_info', server_info
        ) as mock_server_info:
            output = self.client.upload_dataset(
                project_id=self._project_name,
                dataset_id=self._dataset_name,
                dataset={
                    'train': pd.read_csv(self._data_path),
                    'test': pd.read_csv(self._data_path),
                },
                info=self._info,
                is_sync=True,
            )
        self.assertDictEqual(output, response)
        _, kwargs = upload_dataset_patcher.call_args
        files = kwargs.get('files')
        self.assertListEqual(['train', 'test'], list(files.keys()))
        self.assertEqual(files['train'].name, 'train.parquet')
        self.assertEqual(files['test'].name, 'test.parquet')

    def test_upload_dataset_df_23_4_parquet_error(self):
        self.requests_mock.get(
            url=self._get_project_url, json=self._get_project_resp, status=HTTPStatus.OK
        )
        upload_dataset_patcher = mock.patch(
            'fiddler.api.dataset_mixin.DatasetMixin.upload_dataset_from_file'
        ).start()
        response = {
            'uuid': self._job_uuid,
            'name': 'Ingestion dataset Upload',
            'status': 'SUCCESS',
            'progress': 100.0,
            'error_message': None,
        }
        upload_dataset_patcher.return_value = response
        server_info = ServerInfo(**{'feature_flags': {}, 'server_version': '23.4.0'})
        with mock.patch.object(
            self.client, 'server_info', server_info
        ) as mock_server_info:
            output = self.client.upload_dataset(
                project_id=self._project_name,
                dataset_id=self._dataset_name,
                dataset={
                    'train': pd.DataFrame({'col1': ['string', 123]}),
                    'test': pd.read_csv(self._datasets_path.joinpath('dataset_0.csv')),
                },
                info=self._info,
                is_sync=True,
            )
        self.assertDictEqual(output, response)
        _, kwargs = upload_dataset_patcher.call_args
        files = kwargs.get('files')
        self.assertListEqual(['train', 'test'], list(files.keys()))
        self.assertEqual(files['train'].name, 'train.csv')
        self.assertEqual(files['test'].name, 'test.csv')

    def test_upload_dataset_async(self):
        response_body = deepcopy(self._job_response)
        response_body['data'].update({'status': 'STARTED', 'progress': 0.00})
        self.requests_mock.post(
            url=self._ingest_url, json=self._ingest_resp, status=HTTPStatus.ACCEPTED
        )

        resp = self.client.upload_dataset_from_file(
            project_id=self._project_name,
            dataset_id=self._dataset_name,
            files={
                'train': self._datasets_path.joinpath('dataset_0.csv'),
                'test': self._datasets_path.joinpath('dataset_1.csv'),
            },
            info=self._info,
            is_sync=False,
        )
        self.assertDictEqual(self._ingest_resp.get('data'), resp)

    def test_upload_dataset_norows(self):
        with self.assertRaises(ValueError) as e:  # noqa
            self.client.upload_dataset_from_file(
                self._project_name,
                self._dataset_name,
                files={
                    'train': self._datasets_path.joinpath('dataset_2.csv'),
                },
                info=self._info,
            )

    def test_upload_dataset_nocols(self):
        with self.assertRaises(ValueError) as e:  # noqa
            self.client.upload_dataset_from_file(
                self._project_name,
                self._dataset_name,
                files={
                    'train': self._datasets_path.joinpath('dataset_4.csv'),
                },
                info=self._info,
            )

    def test_upload_dataset_df_empty(self):
        with self.assertRaises(ValueError) as e:  # noqa
            _ = self.client.upload_dataset(
                project_id=self._project_name,
                dataset_id=self._dataset_name,
                dataset={},
            )

    def test_upload_dataset_csv(self):
        upload_dataset_patcher = mock.patch(
            'fiddler.api.dataset_mixin.DatasetMixin.upload_dataset_from_file'
        ).start()
        response = {
            'uuid': self._job_uuid,
            'name': 'Ingestion dataset Upload',
            'status': 'SUCCESS',
            'progress': 100.0,
            'error_message': None,
        }
        upload_dataset_patcher.return_value = response
        files = {
            'train': self._data_path,
            'test': self._data_path,
        }
        output = self.client.upload_dataset_from_csv(
            project_id=self._project_name,
            dataset_id=self._dataset_name,
            files=files,
            info=self._info,
            is_sync=True,
        )
        self.assertDictEqual(output, response)
        upload_dataset_patcher.assert_called_once_with(
            project_id=self._project_name,
            dataset_id=self._dataset_name,
            files=files,
            info=self._info,
            file_type=FileType.CSV,
            file_schema=None,  # Since we don't support file_schema; file_schema = None
            is_sync=True,
        )

    def test_upload_dataset_from_dir(self):
        upload_dataset_patcher = mock.patch(
            'fiddler.api.dataset_mixin.DatasetMixin.upload_dataset_from_file'
        ).start()
        response = {
            'uuid': self._job_uuid,
            'name': 'Ingestion dataset Upload',
            'status': 'SUCCESS',
            'progress': 100.0,
            'error_message': None,
        }
        upload_dataset_patcher.return_value = response
        output = self.client.upload_dataset_from_dir(
            project_id=self._project_name,
            dataset_id=self._dataset_name,
            dataset_dir=self._datasets_path,
            file_type=FileType.CSV,
            file_schema=None,
            is_sync=True,
        )
        self.assertDictEqual(output, response)
        all_args = upload_dataset_patcher.call_args.kwargs
        assert isinstance(all_args['project_id'], str)
        assert isinstance(all_args['dataset_id'], str)
        assert isinstance(all_args['files'], dict)
        assert isinstance(all_args['info'], DatasetInfo)
        assert isinstance(all_args['files']['dataset_0.csv'], Path)


if __name__ == '__main__':
    unittest.main()
