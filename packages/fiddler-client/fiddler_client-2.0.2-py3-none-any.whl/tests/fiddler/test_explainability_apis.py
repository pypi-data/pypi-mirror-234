import json
import unittest

import pandas as pd

from fiddler.api.explainability_mixin import (
    DatasetDataSource,
    RowDataSource,
    SqlSliceQueryDataSource,
)
from tests.fiddler.base import BaseTestCase
from tests.fiddler.helper import get_base_api_response_body


class TestExplainabilityApis(BaseTestCase):
    def setUp(self):
        super().setUp()
        self._project_name = 'test_project'
        self._dataset_name = 'test_dataset'
        self._model_name = 'test_model'

    def test_feature_importance_from_dataset(self):
        url = f'{self._url}/feature-importance'

        mock_response = get_base_api_response_body(data={})
        self.requests_mock.post(url, json=mock_response)

        self.client.get_feature_importance(
            model_id=self._model_name,
            project_id=self._project_name,
            data_source=DatasetDataSource(
                dataset_name='test_dataset', num_samples=None
            ),
            num_refs=None,
            num_iterations=None,
            ci_level=None,
            overwrite_cache=False,
        )

        request_body = json.loads(self.requests_mock.calls[0].request.body)

        self.assertEqual(len(self.requests_mock.calls), 1)
        self.assertEqual(request_body['model_name'], self._model_name)
        self.assertEqual(request_body['project_name'], self._project_name)
        self.assertEqual(request_body['organization_name'], self._org)
        self.assertEqual(
            request_body['data_source']['dataset_name'], self._dataset_name
        )
        self.assertEqual(request_body['data_source']['source_type'], 'DATASET')
        self.assertEqual(request_body['overwrite_cache'], False)

    def test_feature_importance_from_slice(self):
        url = f'{self._url}/feature-importance'

        mock_response = get_base_api_response_body(data={})
        self.requests_mock.post(url, json=mock_response)

        slice_query = 'SELECT * FROM table'  # nosec
        self.client.get_feature_importance(
            model_id=self._model_name,
            project_id=self._project_name,
            data_source=SqlSliceQueryDataSource(
                query=slice_query,
                num_samples=None,
            ),
            num_iterations=None,
            num_refs=None,
            ci_level=None,
            overwrite_cache=False,
        )

        request_body = json.loads(self.requests_mock.calls[0].request.body)

        self.assertEqual(len(self.requests_mock.calls), 1)
        self.assertEqual(request_body['model_name'], self._model_name)
        self.assertEqual(request_body['project_name'], self._project_name)
        self.assertEqual(request_body['organization_name'], self._org)
        self.assertEqual(request_body['data_source']['query'], slice_query)
        self.assertEqual(request_body['data_source']['source_type'], 'SQL_SLICE_QUERY')
        self.assertEqual(request_body['overwrite_cache'], False)

    def test_feature_importance_extra_params(self):
        url = f'{self._url}/feature-importance'

        mock_response = get_base_api_response_body(data={})
        self.requests_mock.post(url, json=mock_response)

        num_samples = 10_000
        num_iterations = 10_000
        num_refs = 10_000
        ci_level = 0.99
        overwrite_cache = True

        self.client.get_feature_importance(
            model_id=self._model_name,
            project_id=self._project_name,
            data_source=DatasetDataSource(
                dataset_name='test_dataset',
                num_samples=num_samples,
            ),
            num_iterations=num_iterations,
            num_refs=num_refs,
            ci_level=ci_level,
            overwrite_cache=overwrite_cache,
        )

        request_body = json.loads(self.requests_mock.calls[0].request.body)

        self.assertEqual(len(self.requests_mock.calls), 1)
        self.assertEqual(request_body['model_name'], self._model_name)
        self.assertEqual(request_body['project_name'], self._project_name)
        self.assertEqual(request_body['organization_name'], self._org)
        self.assertEqual(
            request_body['data_source']['dataset_name'], self._dataset_name
        )
        self.assertEqual(request_body['data_source']['num_samples'], num_samples)
        self.assertEqual(request_body['data_source']['source_type'], 'DATASET')
        self.assertEqual(request_body['num_iterations'], num_iterations)
        self.assertEqual(request_body['num_refs'], num_refs)
        self.assertEqual(request_body['ci_level'], ci_level)
        self.assertEqual(request_body['overwrite_cache'], overwrite_cache)

    def test_feature_impact_from_dataset(self):
        url = f'{self._url}/feature-impact'

        mock_response = get_base_api_response_body(data={})
        self.requests_mock.post(url, json=mock_response)

        self.client.get_feature_impact(
            model_id=self._model_name,
            project_id=self._project_name,
            data_source=DatasetDataSource(
                dataset_name='test_dataset',
                num_samples=None,
            ),
            output_columns=None,
            num_iterations=None,
            num_refs=None,
            ci_level=None,
            min_support=None,
            overwrite_cache=False,
        )

        request_body = json.loads(self.requests_mock.calls[0].request.body)

        self.assertEqual(len(self.requests_mock.calls), 1)
        self.assertEqual(request_body['model_name'], self._model_name)
        self.assertEqual(request_body['project_name'], self._project_name)
        self.assertEqual(request_body['organization_name'], self._org)
        self.assertEqual(
            request_body['data_source']['dataset_name'], self._dataset_name
        )
        self.assertEqual(request_body['data_source']['source_type'], 'DATASET')
        self.assertEqual(request_body['overwrite_cache'], False)

    def test_feature_impact_from_slice(self):
        url = f'{self._url}/feature-impact'

        mock_response = get_base_api_response_body(data={})
        self.requests_mock.post(url, json=mock_response)

        slice_query = 'SELECT * FROM table'  # nosec
        self.client.get_feature_impact(
            model_id=self._model_name,
            project_id=self._project_name,
            data_source=SqlSliceQueryDataSource(
                query=slice_query,
                num_samples=None,
            ),
            output_columns=None,
            num_iterations=None,
            num_refs=None,
            ci_level=None,
            min_support=None,
            overwrite_cache=False,
        )

        request_body = json.loads(self.requests_mock.calls[0].request.body)

        self.assertEqual(len(self.requests_mock.calls), 1)
        self.assertEqual(request_body['model_name'], self._model_name)
        self.assertEqual(request_body['project_name'], self._project_name)
        self.assertEqual(request_body['organization_name'], self._org)
        self.assertEqual(request_body['data_source']['query'], slice_query)
        self.assertEqual(request_body['data_source']['source_type'], 'SQL_SLICE_QUERY')
        self.assertEqual(request_body['overwrite_cache'], False)

    def test_feature_impact_extra_params(self):
        url = f'{self._url}/feature-impact'

        mock_response = get_base_api_response_body(data={})
        self.requests_mock.post(url, json=mock_response)

        output_columns = ['proba_1', 'proba_2']
        num_samples = 10_000
        num_iterations = 10_000
        num_refs = 10_000
        ci_level = 0.99
        min_support = 50
        overwrite_cache = True

        self.client.get_feature_impact(
            model_id=self._model_name,
            project_id=self._project_name,
            data_source=DatasetDataSource(
                dataset_name='test_dataset',
                num_samples=num_samples,
            ),
            output_columns=output_columns,
            num_iterations=num_iterations,
            num_refs=num_refs,
            ci_level=ci_level,
            min_support=min_support,
            overwrite_cache=overwrite_cache,
        )

        request_body = json.loads(self.requests_mock.calls[0].request.body)

        self.assertEqual(len(self.requests_mock.calls), 1)
        self.assertEqual(request_body['model_name'], self._model_name)
        self.assertEqual(request_body['project_name'], self._project_name)
        self.assertEqual(request_body['organization_name'], self._org)
        self.assertEqual(
            request_body['data_source']['dataset_name'], self._dataset_name
        )
        self.assertEqual(request_body['data_source']['source_type'], 'DATASET')
        self.assertEqual(request_body['data_source']['num_samples'], num_samples)
        self.assertEqual(request_body['num_iterations'], num_iterations)
        self.assertEqual(request_body['num_refs'], num_refs)
        self.assertEqual(request_body['ci_level'], ci_level)
        self.assertEqual(request_body['min_support'], min_support)
        self.assertEqual(request_body['overwrite_cache'], overwrite_cache)
        self.assertEqual(request_body['output_columns'], output_columns)

    def test_explain_fiddler_shap(self):
        url = f'{self._url}/explain'

        mock_response = get_base_api_response_body(data={})
        self.requests_mock.post(url, json=mock_response)

        self.client.get_explanation(
            model_id=self._model_name,
            project_id=self._project_name,
            input_data_source=RowDataSource(row={'col_a': 3, 'col_b': 'x'}),
            ref_data_source=DatasetDataSource(
                dataset_name=self._dataset_name, source=None, num_samples=10
            ),
            explanation_type='FIDDLER_SHAP',
            num_permutations=300,
            ci_level=0.95,
            top_n_class=None,
        )

        request_body = json.loads(self.requests_mock.calls[0].request.body)

        self.assertEqual(len(self.requests_mock.calls), 1)
        self.assertEqual(request_body['model_name'], self._model_name)
        self.assertEqual(request_body['project_name'], self._project_name)
        self.assertEqual(request_body['organization_name'], self._org)
        self.assertEqual(
            request_body['ref_data_source']['dataset_name'], self._dataset_name
        )
        self.assertEqual(request_body['ref_data_source']['source_type'], 'DATASET')
        self.assertEqual(request_body['ref_data_source']['num_samples'], 10)
        self.assertEqual(request_body['input_data_source']['source_type'], 'ROW')
        self.assertEqual(request_body['explanation_type'], 'FIDDLER_SHAP')
        self.assertEqual(request_body['num_permutations'], 300)

    def test_fairness(self):
        url = f'{self._url}/fairness'

        mock_response = get_base_api_response_body(data={})
        self.requests_mock.post(url, json=mock_response)

        self.client.get_fairness(
            model_id=self._model_name,
            project_id=self._project_name,
            data_source=DatasetDataSource(
                dataset_name=self._dataset_name, source=None, num_samples=None
            ),
            protected_features=['Gender', 'Race'],
            positive_outcome='Churned',
            score_threshold=0.3,
        )

        request_body = json.loads(self.requests_mock.calls[0].request.body)
        self.assertEqual(len(self.requests_mock.calls), 1)
        self.assertEqual(request_body['model_name'], self._model_name)
        self.assertEqual(request_body['organization_name'], self._org)
        self.assertEqual(
            request_body['data_source']['dataset_name'], self._dataset_name
        )
        self.assertEqual(request_body['data_source']['source_type'], 'DATASET')
        self.assertEqual(request_body['protected_features'], ['Gender', 'Race'])
        self.assertEqual(request_body['positive_outcome'], 'Churned')
        self.assertEqual(request_body['score_threshold'], 0.3)

    def test_slice_query(self):
        url = f'{self._url}/slice-query/fetch'

        data = {
            'meta': {
                'columns': [],
                'dtypes': [],
            },
            'rows': [],
        }

        mock_response = get_base_api_response_body(data=data)
        self.requests_mock.post(url, json=mock_response)

        query = 'select * from test_dataset.test_model'
        self.client.get_slice(
            project_id=self._project_name,
            query=query,
            columns=['Gender', 'Race'],
            sample=True,
            max_rows=10,
        )

        request_body = json.loads(self.requests_mock.calls[0].request.body)
        self.assertEqual(len(self.requests_mock.calls), 1)
        self.assertEqual(request_body['project_name'], self._project_name)
        self.assertEqual(request_body['organization_name'], self._org)
        self.assertEqual(request_body['query'], query)
        self.assertEqual(request_body['columns'], ['Gender', 'Race'])
        self.assertEqual(request_body['sample'], True)
        self.assertEqual(request_body['max_rows'], 10)

    def test_get_predictions(self):
        url = f'{self._url}/predict'

        data = {'predictions': {}}

        mock_response = get_base_api_response_body(data=data)
        self.requests_mock.post(url, json=mock_response)
        df = pd.DataFrame([{'col1': 4, 'col2': 'xyz'}])
        self.client.get_predictions(
            project_id=self._project_name,
            model_id=self._model_name,
            input_df=df,
            chunk_size=10,
        )

        request_body = json.loads(self.requests_mock.calls[0].request.body)
        self.assertEqual(len(self.requests_mock.calls), 1)
        self.assertEqual(request_body['project_name'], self._project_name)
        self.assertEqual(request_body['organization_name'], self._org)
        self.assertEqual(request_body['model_name'], self._model_name)
        self.assertEqual(request_body['data'], [{'col1': 4, 'col2': 'xyz'}])
        self.assertEqual(request_body['chunk_size'], 10)

    def test_get_mutual_information(self):
        url = f'{self._url}/mutual-information'

        mock_response = get_base_api_response_body(data={})
        self.requests_mock.post(url, json=mock_response)

        slice_query = 'SELECT * FROM table'  # nosec

        self.client.get_mutual_information(
            project_id=self._project_name,
            dataset_id=self._dataset_name,
            query=slice_query,
            column_name='feature_1',
            normalized=True,
        )

        request_body = json.loads(self.requests_mock.calls[0].request.body)
        self.assertEqual(len(self.requests_mock.calls), 1)
        self.assertEqual(request_body['dataset_name'], self._dataset_name)
        self.assertEqual(request_body['organization_name'], self._org)
        self.assertEqual(request_body['query'], slice_query)
        self.assertEqual(request_body['column_name'], 'feature_1')
        self.assertEqual(request_body['normalized'], True)


if __name__ == '__main__':
    unittest.main()
