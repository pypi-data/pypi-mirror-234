from http import HTTPStatus
from typing import List

from pydantic import parse_obj_as

from fiddler.libs.http_client import RequestClient
from fiddler.schema.webhook import Webhook
from fiddler.utils.decorators import handle_api_error_response
from fiddler.utils.logger import get_logger
from fiddler.utils.response_handler import (
    APIResponseHandler,
    PaginatedResponseHandler,
)

logger = get_logger(__name__)


class WebhookMixin:
    client: RequestClient
    organization_name: str

    @handle_api_error_response
    def add_webhook(self, name: str, url: str, provider: str) -> Webhook:
        """
        Add a new `Webhook`.

        :params name: name of webhook
        :params url: webhook url
        :params provider: Either 'SLACK' or 'OTHER'

        :returns: Created `Webhook` object.
        """
        request_body = {
            'name': name,
            'url': url,
            'provider': provider,
        }
        response = self.client.post(
            url='webhooks',
            params={'organization_name': self.organization_name},
            data=request_body,
        )
        if response.status_code == HTTPStatus.OK:
            logger.info(f'Webhook created successfully.')
        else:
            logger.info('Webhook creation unsuccessful')
        return Webhook.deserialize(APIResponseHandler(response))

    @handle_api_error_response
    def delete_webhook(self, uuid: str) -> None:
        """
        Delete a webhook

        :params uuid: uuid of the Webhook to delete
        :returns: None
        """
        response = self.client.delete(url=f'webhooks/{uuid}')
        if response.status_code == HTTPStatus.OK:
            logger.info(f'Webhook {uuid} deleted successfully.')
        else:
            logger.info('Webhook deletion unsuccessful')

    @handle_api_error_response
    def get_webhook(self, uuid: str) -> List[Webhook]:
        """
        Get a webhook

        :params uuid: UUID belongs to the Webhook
        :returns: `Webhook` object
        """
        response = self.client.get(
            url=f'webhooks/{uuid}',
        )
        return Webhook.deserialize(APIResponseHandler(response))

    @handle_api_error_response
    def update_webhook(self, uuid: str, name: str, url: str, provider: str) -> Webhook:
        """
        Update a webhook, by changing one or more of name, url or provider.
        :params name: name of webhook
        :params url: webhook url
        :params provider: Either 'SLACK' or 'OTHER'

        :returns: Updated `Webhook` object.
        """
        request_body = Webhook(name=name, url=url, provider=provider).dict()
        response = self.client.patch(
            url=f'webhooks/{uuid}',
            data=request_body,
        )
        if response.status_code == HTTPStatus.OK:
            logger.info(f'Webhook {uuid} updated successfully.')
        else:
            logger.info('Webhook updation unsuccessful')
        return Webhook.deserialize(APIResponseHandler(response))

    @handle_api_error_response
    def get_webhooks(self, limit: int = 300, offset: int = 0) -> List[Webhook]:
        """
        Get a list of all webhooks in the organization

        :params limit: Number of webhooks to fetch in a call
        :params offset: Number of rows to skip before any rows are retrived
        :returns: List of `Webhook` object
        """
        response = self.client.get(
            url='webhooks',
            params={
                'organization_name': self.organization_name,
                'limit': limit,
                'offset': offset,
            },
        )
        items = PaginatedResponseHandler(response).get_pagination_items()
        return parse_obj_as(List[Webhook], items)
