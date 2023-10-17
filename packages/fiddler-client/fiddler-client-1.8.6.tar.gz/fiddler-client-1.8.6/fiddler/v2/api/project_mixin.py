from http import HTTPStatus
from typing import List

from pydantic import parse_obj_as

from fiddler.libs.http_client import RequestClient
from fiddler.utils import logging
from fiddler.v2.schema.project import Project
from fiddler.v2.utils.exceptions import handle_api_error_response
from fiddler.v2.utils.response_handler import (
    APIResponseHandler,
    PaginatedResponseHandler,
)

logger = logging.getLogger(__name__)


class ProjectMixin:
    client: RequestClient
    organization_name: str

    @handle_api_error_response
    def get_projects(self, limit: int = 300, offset: int = 0) -> List[Project]:
        """
        Get a list of all projects in the organization

        :params limit: Number of projects to fetch in a call
        :params offset: Number of rows to skip before any rows are retrived
        :returns: List of `Project` object
        """
        response = self.client.get(
            url='projects',
            params={
                'organization_name': self.organization_name,
                'limit': limit,
                'offset': offset,
            },
        )
        # @TODO:  abstracted as an iter object so user doesn't have to manage pagination manually
        _, items = PaginatedResponseHandler(response).get_pagination_details_and_items()
        return parse_obj_as(List[Project], items)

    @handle_api_error_response
    def delete_project(self, project_name: str) -> None:
        """
        Delete a project

        :params project_name: Name of the project to delete
        :returns: None
        """
        response = self.client.delete(
            url=f'projects/{self.organization_name}:{project_name}'
        )
        if response.status_code == HTTPStatus.OK:
            logger.info(f'{project_name} deleted successfully.')
        else:
            # @TODO: Handle non 200 status response
            logger.info('Delete unsuccessful')

    @handle_api_error_response
    def add_project(self, project_name: str) -> Project:
        """
        Add a new project.

        :param project_name: The unique identifier of the project on the
            Fiddler engine. Must be a short string without whitespace.

        :returns: Created `Project` object.
        """
        request_body = Project(
            name=project_name, organization_name=self.organization_name
        ).dict()
        response = self.client.post(
            url='projects',
            params={'organization_name': self.organization_name},
            data=request_body,
        )
        logger.info(f'{project_name} created successfully!')
        return Project.deserialize(APIResponseHandler(response))
