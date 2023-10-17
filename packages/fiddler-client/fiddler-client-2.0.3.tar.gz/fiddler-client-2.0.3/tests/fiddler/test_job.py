import unittest
from typing import Optional

from fiddler.exceptions import AsyncJobFailed
from fiddler.schema.job import JobStatus
from tests.fiddler.base import BaseTestCase


class TestJob(BaseTestCase):
    def setUp(self) -> None:
        super(TestJob, self).setUp()
        self._job_uuid = '3fa85f64-5717-4562-b3fc-2c963f66afa6'
        self._jobs_url = f'{self._url}/jobs/{self._job_uuid}'

    def _get_sample_response_body(
        self, uuid: str, status: str = JobStatus.STARTED, error: Optional[str] = None
    ) -> dict:
        return {
            'api_version': '2.0.0',
            'data': {
                'uuid': uuid,
                'name': 'Upload dataset',
                'status': status,
                'progress': 0.00,
                'error_message': error,
                'extra': {
                    'd16b91f9-6771-4e10-8973-4a15cfd94060': {
                        'status': 'STARTED',
                        'result': {},
                        'error_message': None,
                    },
                    'e2459a4a-c6ee-400f-9dd9-ffc71c6a3e11': {
                        'status': 'STARTED',
                        'result': {},
                        'error_message': None,
                    },
                    'f4498ea9-8e6b-459d-8c31-567352cc085f': {
                        'status': 'STARTED',
                        'result': {},
                        'error_message': None,
                    },
                    '5fdca62c-41eb-4ed8-9b4c-37c1c8e722e7': {
                        'status': 'SUCCESS',
                        'result': {
                            'result': {
                                'task_identifier': '707be37d-24fc-4b32-8279-cc17e89bb3fb',
                                '__org': 'nihardev1f2',
                                '__project': 'bank_churn',
                                '__model': 'bank_churn',
                                '__source_type': '.csv',
                                'file_type': '.csv',
                                '__batch_id': '621b64f7-1e51-4c59-a1ff-13735a687908',
                                'timestamp_field': None,
                                'id_field': None,
                                'is_update': False,
                                '__event_type': 'execution_event',
                                's3_bucket': 'fiddler-bucket-dev',
                                's3_key': 'nihardev1f2//nihardev1f2/bank_churn/bank_churn/event/jdxbz_tmpgupokc42-0.csv',
                                'start_time': 1655291145.9128551,
                                'cleaned_s3_key': 'nihardev1f2//nihardev1f2/bank_churn/bank_churn/event/cleaned/jdxbz_tmpgupokc42-0.csv',
                                'violations_s3_key': 'nihardev1f2//nihardev1f2/bank_churn/bank_churn/event/violations/jdxbz_tmpgupokc42-0.csv',
                                'cleaned_ch_table': 'nihardev1f2__bank_churn__bank_churn',
                                'violations_ch_table': 'nihardev1f2__bank_churn__bank_churn',
                            }
                        },
                        'error_message': None,
                    },
                },
            },
            'kind': 'NORMAL',
        }

    def test_job_running_success(self):
        response_body_0 = self._get_sample_response_body(self._job_uuid)

        response_body_1 = self._get_sample_response_body(self._job_uuid)
        response_body_1['data'].update(progress=50.34232)

        response_body_2 = self._get_sample_response_body(
            self._job_uuid, status=JobStatus.SUCCESS
        )

        self.requests_mock.get(self._jobs_url, json=response_body_0)
        self.requests_mock.get(self._jobs_url, json=response_body_1)
        self.requests_mock.get(self._jobs_url, json=response_body_2)

        self.client.wait_for_job(self._job_uuid, 1)

        self.assertTrue(self.requests_mock.assert_call_count(self._jobs_url, count=3))

    def test_job_fail(self):
        response_body = self._get_sample_response_body(
            self._job_uuid, status=JobStatus.FAILURE, error='test_error'
        )

        self.requests_mock.get(self._jobs_url, json=response_body)

        with self.assertRaises(AsyncJobFailed) as e:
            self.client.wait_for_job(self._job_uuid)
        self.assertEqual(
            str(e.exception),
            'JOB UUID: 3fa85f64-5717-4562-b3fc-2c963f66afa6 failed with Exception: test_error',
        )

        self.assertTrue(self.requests_mock.assert_call_count(self._jobs_url, 1))


if __name__ == '__main__':
    unittest.main()
