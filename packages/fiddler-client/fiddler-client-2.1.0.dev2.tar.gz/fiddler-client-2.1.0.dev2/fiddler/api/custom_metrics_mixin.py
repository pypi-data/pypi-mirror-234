from http import HTTPStatus
from typing import List

from pydantic import parse_obj_as

from fiddler.libs.http_client import RequestClient
from fiddler.schema.custom_metric import CustomMetric
from fiddler.utils.decorators import handle_api_error_response
from fiddler.utils.logger import get_logger
from fiddler.utils.response_handler import (
    APIResponseHandler,
    PaginatedResponseHandler,
)

logger = get_logger(__name__)


class CustomMetricsMixin:

    client: RequestClient
    organization_name: str

    @handle_api_error_response
    def add_custom_metric(
        self, name: str, project_id: str, model_id: str, fql: str
    ) -> CustomMetric:
        """
        Add a new `Custom Metric`.

        :params name: name of custom metric
        :params project_id: name of project
        :params model_id: name of model
        :params fql: The FQL expression describing the metric

        :returns: Created `CustomMetric` object.
        """
        attrs = {
            'organization_name': self.organization_name,
            'project_name': project_id,
            'model_name': model_id,
            'name': name,
            'fql': fql,
        }
        response = self.client.post(
            url='custom-metrics',
            data=attrs,
        )
        response_data = APIResponseHandler(response)
        metric_id = response_data.get_data().get('id')
        attrs['id'] = metric_id
        return CustomMetric.parse_obj(attrs)

    @handle_api_error_response
    def delete_custom_metric(self, metric_id: str = None) -> None:
        """
        Delete a custom metric

        :params uuid: uuid of the custom metric to delete
        :returns: None
        """
        response = self.client.delete(
            url=f'custom-metrics/{metric_id}'
        )
        if response.status_code == HTTPStatus.OK:
            logger.info(f'Custom metric {metric_id} deleted successfully.')
        else:
            logger.info('Custom metric deletion unsuccessful')

    @handle_api_error_response
    def get_custom_metrics(
        self,
        project_id: str,
        model_id: str,
        limit: int = 300,
        offset: int = 0
    ) -> List[CustomMetric]:
        """
        Get a list of `CustomMetric` objects.

        :params project_id: name of project
        :params model_id: name of model

        :returns: a list of `CustomMetric` objects
        """
        params = {
            'organization_name': self.organization_name,
            'project_name': project_id,
            'model_name': model_id,
            'offset': offset,
            'limit': limit,
        }
        response = self.client.get(
            url=f'custom-metrics',
            params=params
        )
        items = PaginatedResponseHandler(response).get_pagination_items()
        return parse_obj_as(List[CustomMetric], items)
