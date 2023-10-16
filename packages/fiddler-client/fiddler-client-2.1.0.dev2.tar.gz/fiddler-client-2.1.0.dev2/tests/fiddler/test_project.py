import unittest
from http import HTTPStatus
from typing import Tuple

from responses import matchers

from fiddler.exceptions import (
    BadRequest,
    Conflict,
    NotFound,
)
from fiddler.schema.project import Project
from tests.fiddler.base import BaseTestCase


class TestProject(BaseTestCase):
    def setUp(self):
        super(TestProject, self).setUp()
        self._project_name = 'test_project'

    def _get_url_query_params(self, project_name: str = None) -> Tuple[str, dict]:
        base_url = f'{self._url}/projects'

        if project_name:
            return f'{base_url}/{self._org}:{project_name}', {}
        return base_url, {'organization_name': self._org}

    def _create_project_dict(self, name: str) -> dict:
        return {'name': name, 'organization_name': self._org}

    def test_get_projects(self):
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
                        'name': 'project_1',
                        'organization_name': self._org,
                        'created_at': '2022-05-19T18:20:25.991688+00:00',
                        'updated_at': '2022-05-19T18:20:25.991688+00:00',
                    },
                    {
                        'id': 1,
                        'name': 'project_2',
                        'organization_name': self._org,
                        'created_at': '2022-05-19T18:22:56.248405+00:00',
                        'updated_at': '2022-05-19T18:22:56.248405+00:00',
                    },
                    {
                        'id': 2,
                        'name': 'project_3',
                        'organization_name': self._org,
                        'created_at': '2022-05-19T20:11:32.338040+00:00',
                        'updated_at': '2022-05-19T20:11:32.338046+00:00',
                    },
                ],
            },
            'api_version': '2.0',
            'kind': 'PAGINATED',
        }
        url, query_params = self._get_url_query_params()
        query_params.update({'limit': 300, 'offset': 0})

        self.requests_mock.get(
            url, json=response, match=[matchers.query_param_matcher(query_params)]
        )

        projects = self.client.get_projects()
        self.assertIsInstance(projects[0], Project)
        self.assertEqual(projects[0].name, 'project_1')
        self.assertEqual(projects[0].organization_name, self._org)
        self.assertEqual(len(projects), 3)

    def test_add_project(self):
        name = 'test_project'

        response_body = {
            'data': {
                'id': 0,
                'name': name,
                'organization_name': self._org,
                'created_at': '2022-05-30T04:54:36.457756+00:00',
                'updated_at': '2022-05-30T04:54:36.457756+00:00',
            },
            'api_version': '2.0',
            'kind': 'NORMAL',
        }

        url, query_params = self._get_url_query_params()

        self.requests_mock.post(
            url, json=response_body, match=[matchers.query_param_matcher(query_params)]
        )

        project = self.client.add_project(project_id=name)
        self.assertIsInstance(project, Project)
        self.assertEqual(project.name, name)
        self.assertEqual(project.organization_name, self._org)

    def test_add_project_409(self):
        name = 'test_project'
        message = 'Project with the same name already exists'
        response_body = {
            'error': {
                'code': 409,
                'message': message,
                'errors': [
                    {
                        'reason': 'Conflict',
                        'message': 'Project with the same name already exists',
                        'help': '',
                    }
                ],
            },
            'api_version': '2.0',
            'kind': 'ERROR',
        }
        url, query_params = self._get_url_query_params()
        self.requests_mock.post(
            url,
            json=response_body,
            match=[matchers.query_param_matcher(query_params)],
            status=HTTPStatus.CONFLICT,
        )

        with self.assertRaises(Conflict) as e:  # noqa
            _ = self.client.add_project(project_id=name)

        self.assertEqual(e.exception.message, message)

    def test_project_bad_request(self):
        message = 'organization_name not specified'
        response_body = {
            'error': {
                'code': HTTPStatus.BAD_REQUEST,
                'message': message,
                'errors': [{'reason': 'BadRequest', 'message': message, 'help': ''}],
            },
            'api_version': '2.0',
            'kind': 'ERROR',
        }
        url, query_params = self._get_url_query_params()
        self.requests_mock.post(
            url,
            json=response_body,
            match=[matchers.query_param_matcher(query_params)],
            status=HTTPStatus.BAD_REQUEST,
        )

        with self.assertRaises(BadRequest) as e:  # noqa
            _ = self.client.add_project(project_id='foo')
            self.assertEqual(e.exception.message, message)

    def test_delete_project(self):
        url, _ = self._get_url_query_params(project_name=self._project_name)
        self.requests_mock.delete(url)
        response = self.client.delete_project(project_id=self._project_name)
        self.assertIsNone(response)

    def test_delete_project_404(self):
        url, _ = self._get_url_query_params(project_name=self._project_name)
        message = (
            "Project({'name': "
            + self._project_name
            + ", 'organization_name': "
            + self._org
            + '}) not found'
        )
        response_body = {
            'error': {
                'code': HTTPStatus.NOT_FOUND,
                'message': message,
                'errors': [
                    {'reason': 'ObjectNotFound', 'message': message, 'help': ''}
                ],
            },
            'api_version': '2.0',
            'kind': 'ERROR',
        }
        self.requests_mock.delete(url, json=response_body, status=HTTPStatus.NOT_FOUND)
        with self.assertRaises(NotFound) as e:
            _ = self.client.delete_project(project_id=self._project_name)

        self.assertEqual(e.exception.message, message)


if __name__ == '__main__':
    unittest.main()
