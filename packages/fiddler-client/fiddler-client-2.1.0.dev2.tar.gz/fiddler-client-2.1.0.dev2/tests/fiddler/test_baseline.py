import unittest
from http import HTTPStatus
from typing import List
from unittest.mock import patch

from fiddler.core_objects import BaselineType
from fiddler.exceptions import (
    BadRequest,
    NotFound,
)
from fiddler.schema.baseline import Baseline
from tests.fiddler.base import BaseTestCase
from tests.fiddler.helper import (
    get_404_error_response,
    get_base_api_response_body,
    get_base_paginated_api_response_body,
)


class TestBaseline(BaseTestCase):
    def setUp(self):
        super(TestBaseline, self).setUp()
        self._project_id = 'test_project'
        self._baseline_id = 'test_baseline'
        self._model_id = 'test_model'
        self._dataset_id = 'test-dataset'

    def _get_url_query_params(
        self,
        organization_id: str = None,
        project_id: str = None,
        baseline_id: str = None,
        model_id: str = None,
    ) -> str:
        base_url = f'{self._url}/baselines'
        if organization_id and project_id and model_id and baseline_id:
            return f'{base_url}?organization_name={organization_id}&project_name={project_id}&model_name={model_id}&baseline_name={baseline_id}'

        if organization_id and project_id and model_id:
            return f'{base_url}?organization_name={organization_id}&project_name={project_id}&model_name={model_id}'

        if organization_id and project_id:
            return f'{base_url}?organization_name={organization_id}&project_name={project_id}'

        if organization_id:
            return f'{base_url}?organization_name={organization_id}'

        return base_url

    def _get_paginated_response_json(self, item_count=3):
        response = get_base_paginated_api_response_body(
            items=[
                self._create_baseline_dict(
                    id=i,
                    name=f'baseline_{i}',
                    type=BaselineType.PRE_PRODUCTION.value,
                    dataset_id=self._dataset_id,
                )
                for i in range(item_count)
            ],
            item_count=item_count,
        )
        return response

    def _create_baseline_dict(
        self,
        id: int,
        name: str,
        type: str,
        dataset_id: str = None,
        start_time=None,
        end_time=None,
        offset=None,
        window_size=None,
    ):
        return {
            'id': id,
            'name': name,
            'organization_name': self._org,
            'project_name': self._project_id,
            'type': type,
            'model_name': self._model_id,
            'dataset_name': dataset_id,
            'start_time': start_time,
            'end_time': end_time,
            'offset': offset,
            'window_size': window_size,
        }

    def test_add_baseline(self):
        id = 0
        response_body = get_base_api_response_body(
            data=self._create_baseline_dict(
                id=id,
                name=self._baseline_id,
                type=BaselineType.PRE_PRODUCTION,
                dataset_id=self._dataset_id,
            ),
        )

        url = self._get_url_query_params()

        self.requests_mock.post(url, json=response_body)

        baseline = self.client.add_baseline(
            self._project_id,
            self._model_id,
            self._baseline_id,
            type=BaselineType.PRE_PRODUCTION,
            dataset_id=self._dataset_id,
        )

        self.assertIsInstance(baseline, Baseline)
        self.assertEqual(baseline.id, id)
        self.assertEqual(baseline.name, self._baseline_id)
        self.assertEqual(baseline.type, BaselineType.PRE_PRODUCTION)
        self.assertEqual(baseline.dataset_name, self._dataset_id)

    @patch('fiddler.api.baseline_mixin.RequestClient.post')
    def test_baseline_construction_add_baseline(self, post_request):
        test_ds_id = self._dataset_id
        baseline = self.client.add_baseline(
            project_id=self._project_id,
            model_id=self._model_id,
            baseline_id=self._baseline_id,
            type=BaselineType.PRE_PRODUCTION,
            dataset_id=test_ds_id,
        )
        post_request.assert_called_once_with(
            url='baselines',
            data={
                'project_name': self._project_id,
                'organization_name': self._org,
                'name': self._baseline_id,
                'dataset_name': test_ds_id,
                'start_time': None,
                'end_time': None,
                'window_size': None,
                'offset': None,
                'model_name': self._model_id,
                'type': BaselineType.PRE_PRODUCTION.value,
                'run_async': True,
            },
        )

    def test_add_baseline_twice_nofail(self):
        id = 0
        response_body = get_base_api_response_body(
            data=self._create_baseline_dict(
                id=id,
                name=self._baseline_id,
                type=BaselineType.PRE_PRODUCTION,
                dataset_id=self._dataset_id,
            ),
        )

        url = self._get_url_query_params()

        self.requests_mock.post(url, json=response_body)

        baseline = self.client.add_baseline(
            self._project_id,
            self._model_id,
            self._baseline_id,
            type=BaselineType.PRE_PRODUCTION,
            dataset_id=self._dataset_id,
        )

        baseline = self.client.add_baseline(
            self._project_id,
            self._model_id,
            self._baseline_id,
            type=BaselineType.PRE_PRODUCTION,
            dataset_id=self._dataset_id,
        )

    def test_add_baseline_different_fail(self):
        id = 0
        response_body = get_base_api_response_body(
            data=self._create_baseline_dict(
                id=id,
                name=self._baseline_id,
                type=BaselineType.PRE_PRODUCTION,
                dataset_id=self._dataset_id,
            ),
        )

        url = self._get_url_query_params()

        self.requests_mock.post(url, json=response_body)
        baseline = self.client.add_baseline(
            self._project_id,
            self._model_id,
            self._baseline_id,
            type=BaselineType.PRE_PRODUCTION,
            dataset_id=self._dataset_id,
        )

        self.requests_mock.post(url, json=response_body, status=HTTPStatus.BAD_REQUEST)
        with self.assertRaises(BadRequest):
            baseline = self.client.add_baseline(
                self._project_id,
                self._model_id,
                self._baseline_id,
                type=BaselineType.PRE_PRODUCTION,
                dataset_id='test_dataset_2',
            )

    def test_add_baseline_no_dataset_name_fail(self):
        id = 0
        response_body = get_base_api_response_body(
            data=self._create_baseline_dict(
                id=id,
                name=self._baseline_id,
                type=BaselineType.PRE_PRODUCTION,
            ),
        )

        url = self._get_url_query_params()

        self.requests_mock.post(url, json=response_body, status=HTTPStatus.BAD_REQUEST)
        with self.assertRaises(BadRequest):
            baseline = self.client.add_baseline(
                self._project_id,
                self._model_id,
                self._baseline_id,
                type=BaselineType.PRE_PRODUCTION,
                dataset_id='test_dataset_2',
            )

    def test_get_baselines(self):
        url = self._get_url_query_params(self._org, self._project_id)
        item_count = 4
        self.requests_mock.get(url, json=self._get_paginated_response_json(item_count))
        baselines = self.client.get_baselines(self._project_id)
        self.assertTrue(isinstance(baselines, List))
        self.assertIsInstance(baselines[0], Baseline)
        self.assertEqual(len(baselines), item_count)

    def test_get_baselines_empty_list(self):
        url = self._get_url_query_params(self._org, self._project_id)
        self.requests_mock.get(url, json=self._get_paginated_response_json(0))
        baselines = self.client.get_baselines(self._project_id)
        self.assertTrue(isinstance(baselines, List))
        self.assertListEqual(baselines, [])

    def test_get_baseline(self):
        id = 0
        response_body = self._get_paginated_response_json(1)

        url = self._get_url_query_params(
            self._org, self._project_id, self._baseline_id, self._model_id
        )

        self.requests_mock.get(url, json=response_body)

        baseline = self.client.get_baseline(
            self._project_id, self._model_id, self._baseline_id
        )

        self.assertIsInstance(baseline, Baseline)
        self.assertEqual(baseline.id, id)
        self.assertEqual(
            baseline.name, 'baseline_0'
        )  # get_paginated_response_json always generates baseline name of the form "baseline_{idx}"
        self.assertEqual(baseline.type, BaselineType.PRE_PRODUCTION)
        self.assertEqual(baseline.dataset_name, self._dataset_id)

    def test_delete_baseline(self):
        url = self._get_url_query_params(
            self._org, self._project_id, self._baseline_id, self._model_id
        )
        self.requests_mock.delete(url, status=HTTPStatus.OK)
        self.client.delete_baseline(self._project_id, self._model_id, self._baseline_id)

        with self.assertRaises(TypeError):
            self.client.delete_baseline(baseline_id=self._baseline_id)

        with self.assertRaises(TypeError):
            self.client.delete_baseline(project_id=self._project_id)

    def test_get_baseline_404(self):
        url = self._get_url_query_params(
            self._org, self._project_id, self._baseline_id, self._model_id
        )
        self.requests_mock.get(
            url, json=get_404_error_response(), status=HTTPStatus.NOT_FOUND
        )
        with self.assertRaises(NotFound) as e:  # noqa
            self.client.get_baseline(
                self._project_id, self._model_id, self._baseline_id
            )


if __name__ == '__main__':
    unittest.main()
