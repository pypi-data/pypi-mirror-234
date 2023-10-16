from responses import matchers
from fiddler.schema.custom_metric import CustomMetric
from fiddler.exceptions import BadRequest
from tests.fiddler.base import BaseTestCase
from http import HTTPStatus


class TestCustomMetric(BaseTestCase):

    def _get_url(self, uuid: str = None) -> str:
        base_url = f'{self._url}/custom-metrics'
        if uuid:
            return f'{base_url}/{uuid}'
        return base_url

    def test_get_custom_metrics(self):
        response = {
            "data": {
                "page_size": 50,
                "total": 2,
                "item_count": 2,
                "page_count": 1,
                "page_index": 1,
                "offset": 0,
                "items": [
                    {
                        "project_name": "bank_churn",
                        "name": "tp_0.8",
                        "model_name": "churn_classifier",
                        "fql": "sum(age)",
                        "id": "fbba0596-1d49-4159-a5ea-e1c2f57c9c32",
                        "organization_name": "test_organization"
                    },
                    {
                        "project_name": "bank_churn",
                        "name": "tp_0.6",
                        "model_name": "churn_classifier",
                        "fql": "sum(credit_score)",
                        "id": "3a352397-a89a-495d-a095-440f1d21a58a",
                        "organization_name": "test_organization"
                    }
                ]
            },
            "api_version": "2.0",
            "kind": "PAGINATED"
        }
        url = self._get_url()
        query_params = {
            'limit': 300,
            'offset': 0,
            'organization_name': 'test_organization',
            'project_name': 'bank_churn',
            'model_name': 'churn_classifier',
        }

        self.requests_mock.get(
            url, json=response, match=[matchers.query_param_matcher(query_params)]
        )

        custom_metrics = self.client.get_custom_metrics(
            project_id='bank_churn',
            model_id='churn_classifier',
        )
        assert custom_metrics == [
            CustomMetric(
                id='fbba0596-1d49-4159-a5ea-e1c2f57c9c32',
                name='tp_0.8',
                fql='sum(age)',
                organization_name='test_organization',
                project_name='bank_churn',
                model_name='churn_classifier',
            ),
            CustomMetric(
                id='3a352397-a89a-495d-a095-440f1d21a58a',
                name='tp_0.6',
                fql='sum(credit_score)',
                organization_name='test_organization',
                project_name='bank_churn',
                model_name='churn_classifier',
            ),
        ]

    def test_add_custom_metric(self):
        response_body = {
            'data': {
                'id': 'fbba0596-1d49-4159-a5ea-e1c2f57c9c32',
            },
            'api_version': '2.0',
            'kind': 'NORMAL',
        }

        url = self._get_url()

        self.requests_mock.post(url, json=response_body)

        custom_metric = self.client.add_custom_metric(
            name='my custom',
            fql='sum(age)',
            project_id='bank_churn',
            model_id='churn_classifier',
        )
        assert custom_metric == CustomMetric(
            id='fbba0596-1d49-4159-a5ea-e1c2f57c9c32',
            name='my custom',
            fql='sum(age)',
            organization_name='test_organization',
            project_name='bank_churn',
            model_name='churn_classifier',
        )

    def test_add_custom_metric_error(self):
        response_body = {
            'error': {
                'code': 400,
                'message': 'Column unknown not found in model churn_classifier',
                'errors': [
                    {
                        'reason': 'CustomMetricInvalidColumn',
                        'message': 'Column unknown not found in model churn_classifier',
                        'help': ''}
                ]
            },
            'api_version': '2.0',
            'kind': 'ERROR'
        }

        url = self._get_url()

        self.requests_mock.post(url, json=response_body, status=HTTPStatus.BAD_REQUEST)

        with self.assertRaises(BadRequest) as context:
            self.client.add_custom_metric(
                name='my custom',
                fql='sum(unknown)',
                project_id='bank_churn',
                model_id='churn_classifier',
            )
        self.assertEqual(
            context.exception.message,
            "Column unknown not found in model churn_classifier"
        )

    def test_delete_custom_metric(self):
        uuid = 'fbba0596-1d49-4159-a5ea-e1c2f57c9c32'
        url = self._get_url(uuid)

        self.requests_mock.delete(url)

        self.client.delete_custom_metric(
            metric_id='fbba0596-1d49-4159-a5ea-e1c2f57c9c32'
        )
        self.assertEqual(len(self.requests_mock.calls), 1)
