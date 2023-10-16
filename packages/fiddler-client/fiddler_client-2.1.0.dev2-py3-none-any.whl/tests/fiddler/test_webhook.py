import json
import unittest
from http import HTTPStatus
from typing import Tuple

from responses import matchers

from fiddler.exceptions import (
    BadRequest,
    Conflict,
    NotFound,
)
from fiddler.schema.webhook import Webhook
from tests.fiddler.base import BaseTestCase


class TestWebhook(BaseTestCase):
    def setUp(self):
        super(TestWebhook, self).setUp()

    def _get_url(self, uuid: str = None) -> str:
        base_url = f'{self._url}/webhooks'
        if uuid:
            return (f'{base_url}/{uuid}',)
        return base_url

    def test_get_webhooks(self):
        response = {
            'data': {
                'page_size': 100,
                'total': 3,
                'item_count': 3,
                'page_count': 1,
                'page_index': 1,
                'offset': 0,
                'items': [
                    {
                        'id': 0,
                        'uuid': 'uuid_0',
                        'name': 'webhook_0',
                        'url': 'url_0',
                        'provider': 'SLACK',
                        'organization_name': 'test_organization',
                        'created_at': '2022-05-19T18:20:25.991688+00:00',
                        'updated_at': '2022-05-19T18:20:25.991688+00:00',
                        'created_by': 'test_user',
                        'updated_by': 'test_user',
                    },
                    {
                        'id': 1,
                        'uuid': 'uuid_1',
                        'name': 'webhook_1',
                        'url': 'url_1',
                        'provider': 'SLACK',
                        'organization_name': 'test_organization',
                        'created_at': '2022-05-19T18:20:25.991688+00:00',
                        'updated_at': '2022-05-19T18:20:25.991688+00:00',
                        'created_by': 'test_user',
                        'updated_by': 'test_user',
                    },
                    {
                        'id': 2,
                        'uuid': 'uuid_2',
                        'name': 'webhook_2',
                        'url': 'url_2',
                        'provider': 'SLACK',
                        'organization_name': 'test_organization',
                        'created_at': '2022-05-19T18:20:25.991688+00:00',
                        'updated_at': '2022-05-19T18:20:25.991688+00:00',
                        'created_by': 'test_user',
                        'updated_by': 'test_user',
                    },
                ],
            },
            'api_version': '2.0',
            'kind': 'PAGINATED',
        }
        url = self._get_url()
        query_params = {
            'limit': 300,
            'offset': 0,
            'organization_name': 'test_organization',
        }

        self.requests_mock.get(
            url, json=response, match=[matchers.query_param_matcher(query_params)]
        )

        webhooks = self.client.get_webhooks()
        self.assertIsInstance(webhooks[0], Webhook)
        self.assertEqual(webhooks[0].name, 'webhook_0')
        self.assertEqual(webhooks[0].organization_name, self._org)
        self.assertEqual(len(webhooks), 3)

    def test_add_webhook(self):
        response_body = {
            'data': {
                'id': 0,
                'uuid': 'uuid_0',
                'name': 'webhook_0',
                'url': 'url_0',
                'provider': 'SLACK',
                'organization_name': 'test_organization',
                'created_at': '2022-05-19T18:20:25.991688+00:00',
                'updated_at': '2022-05-19T18:20:25.991688+00:00',
                'created_by': 'test_user',
                'updated_by': 'test_user',
            },
            'api_version': '2.0',
            'kind': 'NORMAL',
        }

        url = self._get_url()
        query_params = {'organization_name': 'test_organization'}

        self.requests_mock.post(
            url, json=response_body, match=[matchers.query_param_matcher(query_params)]
        )

        webhook = self.client.add_webhook(
            name='webhook_0', url='url_i', provider='SLACK'
        )
        request_body = json.loads(self.requests_mock.calls[0].request.body)
        self.assertEqual(webhook.uuid, 'uuid_0')
        self.assertEqual(len(self.requests_mock.calls), 1)
        self.assertEqual(request_body['name'], 'webhook_0')
