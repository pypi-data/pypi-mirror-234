import unittest
from http import HTTPStatus
from typing import Dict, List, Tuple

from fiddler.core_objects import DatasetInfo as DatasetInfoObj
from fiddler.exceptions import NotFound
from fiddler.schema.dataset import Dataset, DatasetInfo, DatasetIngest
from tests.fiddler.base import BaseTestCase
from tests.fiddler.helper import (
    get_404_error_response,
    get_base_api_response_body,
    get_base_paginated_api_response_body,
)


class TestDataset(BaseTestCase):
    def setUp(self):
        super(TestDataset, self).setUp()
        self._project_name = 'test_project'
        self._dataset_name = 'test_dataset'
        self._example_info = {
            'name': 'some_name',
            'columns': [
                {
                    'column-name': 'location_state',
                    'data-type': 'category',
                    'possible-values': [
                        'Arizona',
                        'California',
                        'Nevada',
                        'Oregon',
                        'Washington',
                    ],
                    'is-nullable': False,
                },
                {
                    'column-name': 'income',
                    'data-type': 'int',
                    'is-nullable': False,
                    'value-range-min': 0,
                    'value-range-max': 99981,
                },
                {
                    'column-name': 'total_claim_amounttotal_claim_amounttotal_claim_amounttotal_claim_amount',
                    'data-type': 'float',
                    'is-nullable': False,
                    'value-range-min': 0.099007,
                    'value-range-max': 2893.239678,
                },
                {
                    'column-name': 'vehicle_class',
                    'data-type': 'category',
                    'possible-values': [
                        'Four-Door Car',
                        'Luxury Car',
                        'Luxury SUV',
                        'SUV',
                        'Sports Car',
                        'Two-Door Car',
                    ],
                    'is-nullable': False,
                },
            ],
        }
        self._example_file_list = {
            'tree': [
                {
                    'name': 'auto_insurance.yaml',
                    'size': 3456,
                    'modified': 1645229905.6390371,
                },
                {
                    'name': 'baseline.csv.parquet',
                    'size': 231279,
                    'modified': 1645229905.622992,
                },
            ]
        }
        self._file_names = ['auto_insurance.yaml', 'baseline.csv.parquet']

    def _get_url_query_params(
        self, dataset_name: str = None
    ) -> Tuple[str, Dict[str, str]]:
        base_url = f'{self._url}/datasets'
        query_param = {}

        if dataset_name:
            return (
                f'{base_url}/{self._org}:{self._project_name}:{dataset_name}',
                query_param,
            )

        return base_url, {
            'organization_name': self._org,
            'project_name': self._project_name,
        }

    def _get_paginated_response_json(self, item_count=3):
        response = get_base_paginated_api_response_body(
            items=[
                self._create_dataset_dict(id=i, name=f'dataset_{i}')
                for i in range(item_count)
            ],
            item_count=item_count,
        )
        return response

    def _create_dataset_dict(
        self,
        id: int,
        name: str,
        info: dict = None,
        version: str = '0.1',
        file_list: dict = None,
    ):
        return {
            'id': id,
            'name': name,
            'info': info if info else self._example_info,
            'version': version,
            'file_list': file_list if file_list else self._example_file_list,
            'organization_name': self._org,
            'project_name': self._project_name,
        }

    def test_get_datasets(self):
        url, _ = self._get_url_query_params()
        item_count = 4
        self.requests_mock.get(url, json=self._get_paginated_response_json(item_count))
        datasets = self.client.get_datasets(self._project_name)
        self.assertTrue(isinstance(datasets, List))
        self.assertIsInstance(datasets[0], Dataset)
        self.assertEqual(len(datasets), item_count)

    def test_get_datasets_empty_list(self):
        url, _ = self._get_url_query_params()
        self.requests_mock.get(url, json=self._get_paginated_response_json(0))
        datasets = self.client.get_datasets(self._project_name)
        self.assertTrue(isinstance(datasets, List))
        self.assertListEqual(datasets, [])

    def test_get_dataset(self):
        id = 0
        response_body = get_base_api_response_body(
            data=self._create_dataset_dict(
                id=id,
                name=self._dataset_name,
                info=self._example_info,
                file_list=self._example_file_list,
            ),
        )

        url, _ = self._get_url_query_params(self._dataset_name)

        self.requests_mock.get(url, json=response_body)

        dataset = self.client.get_dataset(self._project_name, self._dataset_name)

        self.assertIsInstance(dataset, Dataset)
        self.assertEqual(dataset.id, id)
        self.assertEqual(dataset.name, self._dataset_name)
        self.assertEqual(type(dataset.info), DatasetInfo)
        self.assertDictEqual(dataset.file_list, self._example_file_list)

    def test_get_dataset_404(self):
        url, _ = self._get_url_query_params(self._dataset_name)
        self.requests_mock.get(
            url, json=get_404_error_response(), status=HTTPStatus.NOT_FOUND
        )
        with self.assertRaises(NotFound) as e:  # noqa
            self.client.get_dataset(self._project_name, self._dataset_name)

    def test_DatasetIngest_creation(self):
        request_body = DatasetIngest(
            name=self._dataset_name,
            file_name=self._file_names,
            info=DatasetInfoObj.from_dict(self._example_info),
        ).to_dict()
        assert request_body['info']['columns'] == self._example_info['columns']


if __name__ == '__main__':
    unittest.main()
