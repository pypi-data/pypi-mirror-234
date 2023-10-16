import json
import unittest
from http import HTTPStatus
from pathlib import Path
from unittest import mock

import pandas as pd
from requests import Response

from fiddler.schema.server_info import ServerInfo
from fiddler.api.api import FiddlerClient
from fiddler.constants import FiddlerTimestamp, UploadType
from fiddler.exceptions import HttpException
from tests.fiddler.base import BaseTestCase


class TestEventsAPI(BaseTestCase):
    def setUp(self) -> None:
        super(TestEventsAPI, self).setUp()
        self._project_id = 'test_project'
        self._model_id = 'test_model'
        self._job_uuid = '3fa85f64-5717-4562-b3fc-2c963f66afa6'
        self._jobs_url = f'{self._url}/jobs/{self._job_uuid}'
        self._job_response = {
            'data': {
                'uuid': self._job_uuid,
                'name': 'Ingestion publish events',
                'status': 'SUCCESS',
                'progress': 100.0,
                'error_message': None,
                'extras': {},
            },
            'api_version': '2.0',
            'kind': 'NORMAL',
        }
        self._events_path = Path(__file__).parent.parent.joinpath(
            'datasets', 'data', 'ingest_events.csv'
        )
        self.multipart_upload_patcher = mock.patch(
            'fiddler.api.events_mixin.multipart_upload'
        ).start()
        self.multipart_upload_patcher.return_value = {
            'status': 'SUCCESS',
            'file_name': 'dataset.csv',
            'message': 'Successfully uploaded to blob',
        }
        self._ingest_url = (
            f'{self._url}/events/{self._org}:{self._project_id}:{self._model_id}/ingest'
        )
        self._ingest_resp = {
            'data': {
                'status': HTTPStatus.ACCEPTED,
                'job_uuid': self._job_uuid,
                'files': [],
                'message': 'Successfully received the event data. Please allow time for the event ingestion to complete in the Fiddler platform.',
            },
            'api_version': '2.0',
            'kind': 'NORMAL',
        }
        self._single_event_url = (
            f'events/{self._org}:{self._project_id}:{self._model_id}/ingest/event'
        )

    def test_publish_events_batch_exception_sync(self):
        self.requests_mock.post(
            url=self._ingest_url, body='some error', status=HTTPStatus.OK
        )
        with self.assertRaises(HttpException) as ex:  # noqa
            self.client.publish_events_batch(
                project_id=self._project_id,
                model_id=self._model_id,
                batch_source='',
                events_path=self._events_path,
                wait=True,
            )

    def test_publish_events_batch_sync(self):
        self.requests_mock.get(self._jobs_url, json=self._job_response)
        self.requests_mock.post(
            url=self._ingest_url, json=self._ingest_resp, status=HTTPStatus.ACCEPTED
        )

        output = self.client.publish_events_batch(
            project_id=self._project_id,
            model_id=self._model_id,
            batch_source='',
            events_path=self._events_path,
            wait=True,
        )
        self.assertDictEqual(
            output,
            {
                'uuid': self._job_uuid,
                'name': 'Ingestion publish events',
                'status': 'SUCCESS',
                'progress': 100.0,
                'error_message': None,
            },
        )
        self.multipart_upload_patcher.assert_called_once_with(
            client=mock.ANY,
            organization_name=self._org,
            project_name=self._project_id,
            identifier=self._model_id,
            upload_type=UploadType.EVENT,
            file_path=str(self._events_path),
            file_name=self._events_path.name,
        )

    def test_publish_events_dataframe_sync(self):
        batch_id = None
        id_field = None
        is_update = None
        timestamp_field = None
        timestamp_format = None
        group_by = None
        wait = True
        publish_events_patcher = mock.patch(
            'fiddler.api.events_mixin.EventsMixin.publish_events_batch',
        ).start()
        response = {
            'uuid': self._job_uuid,
            'name': 'Ingestion publish events',
            'status': 'SUCCESS',
            'progress': 100.0,
            'error_message': None,
        }
        publish_events_patcher.return_value = response
        output = self.client._publish_events_batch_dataframe(
            self._project_id,
            self._model_id,
            events_df=pd.read_csv(self._events_path),
            batch_id=batch_id,
            id_field=id_field,
            is_update=is_update,
            timestamp_field=timestamp_field,
            timestamp_format=timestamp_format,
            group_by=group_by,
            wait=wait,
        )
        self.assertDictEqual(output, response)
        publish_events_patcher.assert_called_once_with(
            project_id=self._project_id,
            model_id=self._model_id,
            batch_source=mock.ANY,
            batch_id=batch_id,
            id_field=id_field,
            update_event=is_update,
            timestamp_field=timestamp_field,
            timestamp_format=timestamp_format,
            group_by=group_by,
            wait=wait,
            file_type='.csv',
        )

        _, kwargs = publish_events_patcher.call_args
        events = kwargs.get('batch_source')
        self.assertIsNotNone(events)

    def test_publish_events_dataframe_sync_parquet(self):
        batch_id = None
        id_field = None
        is_update = None
        timestamp_field = None
        timestamp_format = None
        group_by = None
        wait = True
        publish_events_patcher = mock.patch(
            'fiddler.api.events_mixin.EventsMixin.publish_events_batch',
        ).start()
        response = {
            'uuid': self._job_uuid,
            'name': 'Ingestion publish events',
            'status': 'SUCCESS',
            'progress': 100.0,
            'error_message': None,
        }
        publish_events_patcher.return_value = response
        server_info = ServerInfo(**{'feature_flags': {}, 'server_version': '23.4.0'})
        with mock.patch.object(
            self.client, 'server_info', server_info
        ) as mock_server_info:
            output = self.client._publish_events_batch_dataframe(
                self._project_id,
                self._model_id,
                events_df=pd.read_csv(self._events_path),
                batch_id=batch_id,
                id_field=id_field,
                is_update=is_update,
                timestamp_field=timestamp_field,
                timestamp_format=timestamp_format,
                group_by=group_by,
                wait=wait,
            )
        self.assertDictEqual(output, response)
        publish_events_patcher.assert_called_once_with(
            project_id=self._project_id,
            model_id=self._model_id,
            batch_source=mock.ANY,
            batch_id=batch_id,
            id_field=id_field,
            update_event=is_update,
            timestamp_field=timestamp_field,
            timestamp_format=timestamp_format,
            group_by=group_by,
            wait=wait,
            file_type='.parquet',
        )

        _, kwargs = publish_events_patcher.call_args
        events = kwargs.get('batch_source')
        assert events.endswith('.parquet')

    def test_publish_events_dataframe_sync_parquet_failure(self):
        batch_id = None
        id_field = None
        is_update = None
        timestamp_field = None
        timestamp_format = None
        group_by = None
        wait = True
        publish_events_patcher = mock.patch(
            'fiddler.api.events_mixin.EventsMixin.publish_events_batch',
        ).start()
        response = {
            'uuid': self._job_uuid,
            'name': 'Ingestion publish events',
            'status': 'SUCCESS',
            'progress': 100.0,
            'error_message': None,
        }
        publish_events_patcher.return_value = response
        server_info = ServerInfo(**{'feature_flags': {}, 'server_version': '23.4.0'})
        with mock.patch.object(
            self.client, 'server_info', server_info
        ) as mock_server_info:
            output = self.client._publish_events_batch_dataframe(
                self._project_id,
                self._model_id,
                events_df=pd.DataFrame({'col': ['string', 123]}),
                batch_id=batch_id,
                id_field=id_field,
                is_update=is_update,
                timestamp_field=timestamp_field,
                timestamp_format=timestamp_format,
                group_by=group_by,
                wait=wait,
            )
        self.assertDictEqual(output, response)
        publish_events_patcher.assert_called_once_with(
            project_id=self._project_id,
            model_id=self._model_id,
            batch_source=mock.ANY,
            batch_id=batch_id,
            id_field=id_field,
            update_event=is_update,
            timestamp_field=timestamp_field,
            timestamp_format=timestamp_format,
            group_by=group_by,
            wait=wait,
            file_type='.csv',
        )

        _, kwargs = publish_events_patcher.call_args
        events = kwargs.get('batch_source')
        assert events.endswith('.csv')

    def test_publish_event(self):
        self.requests_mock.stop()
        client_mocker = mock.patch('fiddler.api.api.RequestClient').start()
        client = FiddlerClient(self._url, self._org, 'ssds')
        response = Response()
        response.status_code = HTTPStatus.ACCEPTED
        fiddler_id = 'foo'
        response._content = json.dumps(
            {
                'data': {
                    'status': HTTPStatus.ACCEPTED,
                    'message': 'Successfully accepted an event',
                    '__fiddler_id': fiddler_id,
                },
                'api_version': '2.0',
                'kind': 'NORMAL',
            }
        ).encode('utf-8')
        client_mocker.return_value.post.return_value = response

        event = {
            'field_1': 10,
            'field_2': None,
            'field_3': False,
            'field_4': 'str',
            'field_5': '00:00:00',
            'id': 1,
        }

        event_id = '1'
        id_field = 'id'
        is_update = False
        event_timestamp = 'field_5'
        timestamp_format = FiddlerTimestamp.INFER

        resp = client.publish_event(
            self._project_id,
            self._model_id,
            event,
            event_id=event_id,
            id_field=id_field,
            update_event=is_update,
            event_timestamp=event_timestamp,
            timestamp_format=timestamp_format,
        )

        client_mocker.return_value.post.assert_called_once_with(
            url=self._single_event_url,
            data={
                'event': event,
                'event_id': event_id,
                'id_field': id_field,
                'is_update': is_update,
                'event_timestamp': event_timestamp,
                'timestamp_format': timestamp_format,
            },
        )
        self.assertEqual(resp, fiddler_id)

    def test_publish_event_exception(self):
        self.requests_mock.post(
            url=f'{self._url}/{self._single_event_url}',
            body='this is error',
            status=HTTPStatus.OK,
        )
        with self.assertRaises(HttpException):
            self.client.publish_event(
                project_id=self._project_id, model_id=self._model_id, event={}
            )


if __name__ == '__main__':
    unittest.main()
