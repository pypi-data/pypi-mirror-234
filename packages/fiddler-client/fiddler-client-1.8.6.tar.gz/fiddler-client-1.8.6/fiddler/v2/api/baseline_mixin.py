from http import HTTPStatus
from typing import List

from pydantic import parse_obj_as

from fiddler.core_objects import BaselineType, WindowSize
from fiddler.libs.http_client import RequestClient
from fiddler.utils import logging
from fiddler.v2.schema.baseline import Baseline
from fiddler.v2.utils.exceptions import handle_api_error_response
from fiddler.v2.utils.response_handler import (
    APIResponseHandler,
    PaginatedResponseHandler,
)

logger = logging.getLogger(__name__)


class BaselineMixin:
    client: RequestClient
    organization_name: str

    @handle_api_error_response
    def list_baselines(self, project_id: str, model_id: str = None) -> List[Baseline]:
        """Get list of all Baselines at project or model level

        :param project_id: unique identifier for the project
        :type project_id: string
        :param model_id: (optional) unique identifier for the model
        :type model_id: string
        :returns: List containing Baseline objects
        """
        response = self.client.get(
            url='baselines',
            params={
                'organization_name': self.organization_name,
                'project_name': project_id,
                'model_name': model_id,
            },
        )
        _, items = PaginatedResponseHandler(response).get_pagination_details_and_items()
        return parse_obj_as(List[Baseline], items)

    @handle_api_error_response
    def get_baseline(
        self, project_id: str, model_id: str, baseline_id: str
    ) -> Baseline:
        """Get the details of a Baseline.

        :param project_id: unique identifier for the project
        :type project_id: string
        :param model_id: unique identifier for the model
        :type model_id: string
        :param baseline_id: unique identifier for the baseline
        :type baseline_id: string

        :returns: Baseline object which contains the details
        """
        response = self.client.get(
            url='baselines',
            params={
                'organization_name': self.organization_name,
                'project_name': project_id,
                'model_name': model_id,
                'baseline_name': baseline_id,
            },
        )
        _, items = PaginatedResponseHandler(response).get_pagination_details_and_items()

        # If a baseline exists, only a single baseline should be returned
        if len(items) == 1:
            return parse_obj_as(Baseline, items[0])
        else:
            return None

    @handle_api_error_response
    def add_baseline(
        self,
        project_id: str,
        model_id: str,
        baseline_id: str,
        type: BaselineType,
        dataset_id: str = None,
        start_time: int = None,
        end_time: int = None,
        offset: WindowSize = None,
        window_size: WindowSize = None,
    ) -> Baseline:
        """Function to add a Baseline to fiddler for monitoring

        :param project_id: unique identifier for the project
        :type project_id: string
        :param model_id: unique identifier for the model
        :type model_id: string
        :param baseline_id: unique identifier for the baseline
        :type baseline_id: string
        :param type: type of the Baseline
        :type type: BaselineType
        :param dataset_id: (optional) dataset to be used as baseline
        :type dataset_id: string
        :param start_time: (optional) seconds since epoch to be used as start time for STATIC_PRODUCTION baseline
        :type start_time: int
        :param end_time: (optional) seconds since epoch to be used as end time for STATIC_PRODUCTION baseline
        :type end_time: int
        :param offset: (optional) offset in seconds relative to current time to be used for ROLLING_PRODUCTION baseline
        :type offset: WindowSize
        :param window_size: (optional) width of window in seconds to be used for ROLLING_PRODUCTION baseline
        :type window_size: WindowSize


        :return: Baseline object which contains the Baseline details
        """
        if window_size:
            window_size = int(window_size)  # ensure enum is converted to int

        request_body = Baseline(
            organization_name=self.organization_name,
            project_name=project_id,
            name=baseline_id,
            type=str(type),
            model_name=model_id,
            dataset_name=dataset_id,
            start_time=start_time,
            end_time=end_time,
            offset=offset,
            window_size=window_size,
        ).dict()

        if 'id' in request_body:
            request_body.pop('id')

        response = self.client.post(
            url='baselines',
            data=request_body,
        )

        if response.status_code == HTTPStatus.OK:
            logger.info(f'{baseline_id} setup successful')
            return Baseline.deserialize(APIResponseHandler(response))

    @handle_api_error_response
    def delete_baseline(self, project_id: str, model_id: str, baseline_id: str) -> None:
        """Delete a Baseline

        :param project_id: unique identifier for the project
        :type project_id: string
        :param model_id: unique identifier for the model
        :type model_id: string
        :param baseline_id: unique identifier for the baseline
        :type baseline_id: string

        :returns: None
        """
        response = self.client.delete(
            url='baselines',
            params={
                'organization_name': self.organization_name,
                'project_name': project_id,
                'model_name': model_id,
                'baseline_name': baseline_id,
            },
        )

        if response.status_code == HTTPStatus.OK:
            logger.info(f'{baseline_id} delete request received.')
        else:
            # @TODO: Handle non 200 status response
            logger.info('Delete unsuccessful')
