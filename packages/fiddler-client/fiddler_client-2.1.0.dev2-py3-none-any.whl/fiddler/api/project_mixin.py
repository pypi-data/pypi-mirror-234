from http import HTTPStatus
from typing import List

from pydantic import parse_obj_as

from fiddler.libs.http_client import RequestClient
from fiddler.schema.project import Project
from fiddler.utils.decorators import handle_api_error_response
from fiddler.utils.logger import get_logger
from fiddler.utils.response_handler import (
    APIResponseHandler,
    PaginatedResponseHandler,
)

logger = get_logger(__name__)


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
        items = PaginatedResponseHandler(response).get_pagination_items()
        return parse_obj_as(List[Project], items)

    # Projects
    def get_project_names(self) -> List[str]:
        """
        List the ids of all projects in the organization.

        :returns: List of strings containing the ids of each project.
        """
        projects = self.get_projects()
        return [project.name for project in projects]

    def list_projects(self) -> List[str]:
        """
        List the ids of all projects in the organization.

        :returns: List of strings containing the ids of each project.
        """
        return self.get_project_names()

    @handle_api_error_response
    def delete_project(self, project_id: str) -> None:
        """
        Delete a project

        :params project_id: Name of the project to delete
        :returns: None
        """

        response = self.client.delete(
            url=f'projects/{self.organization_name}:{project_id}'
        )
        if response.status_code == HTTPStatus.OK:
            logger.info(f'{project_id} deleted successfully.')
        else:
            # @TODO: Handle non 200 status response
            logger.info('Delete unsuccessful')

    @handle_api_error_response
    def add_project(self, project_id: str) -> Project:
        """
        Add a new project.

        :param project_id: The unique identifier of the project on the
            Fiddler engine. Must be a short string without whitespace.

        :returns: Created `Project` object.
        """
        request_body = Project(
            name=project_id, organization_name=self.organization_name
        ).dict()
        response = self.client.post(
            url='projects',
            params={'organization_name': self.organization_name},
            data=request_body,
        )
        logger.info(f'{project_id} created successfully!')
        return Project.deserialize(APIResponseHandler(response))

    create_project = add_project
