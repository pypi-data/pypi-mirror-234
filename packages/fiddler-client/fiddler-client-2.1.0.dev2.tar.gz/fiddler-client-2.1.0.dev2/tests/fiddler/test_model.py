from http import HTTPStatus
from typing import Dict, Tuple

from responses import matchers

from fiddler.exceptions import NotFound
from fiddler.schema.model import Model
from tests.fiddler.base import BaseTestCase
from tests.fiddler.helper import (
    get_404_error_response,
    get_base_api_response_body,
    get_base_paginated_api_response_body,
)


class TestModel(BaseTestCase):
    def setUp(self):
        super(TestModel, self).setUp()
        self._project_name = 'test_project'
        self._model_name = 'test_model'
        self._example_model_info_dict = {
            'name': 'IMDB Sentiment Classifier',
            'input-type': 'text',
            'model-task': 'binary_classification',
            'inputs': [
                {'column-name': 'sentence', 'data-type': 'str', 'is-nullable': False}
            ],
            'outputs': [
                {
                    'column-name': 'sentiment',
                    'data-type': 'float',
                    'is-nullable': False,
                    'value-range-min': 0.0,
                    'value-range-max': 1.0,
                }
            ],
            'datasets': ['imdb_rnn'],
            'target-class-order': [False, True],
            'targets': [
                {
                    'column-name': 'polarity',
                    'data-type': 'bool',
                    'possible-values': [False, True],
                    'is-nullable': False,
                }
            ],
            'description': 'imdb rnn sentiment classifier',
            'preferred-explanation-method': 'ig_flex',
            'binary_classification_threshold': 0.5,
            'schema_version': '0.0',
            'custom-explanation-names': [],
        }
        self._example_file_list_dict = [
            {'name': '__init__.py', 'size': 0, 'modified': 1652585533.11354},
            {'name': 'model.yaml', 'size': 699, 'modified': 1652984684.5440269},
            {'name': 'package.py', 'size': 3396, 'modified': 1652585533.11354},
            {'name': 'saved_model', 'size': 70, 'modified': 1652585533.1175401},
            {
                'name': 'tokenizer.pkl',
                'size': 4326960,
                'modified': 1652585533.1495402,
            },
        ]

    def _get_url_query_params(
        self, model_name: str = None
    ) -> Tuple[str, Dict[str, str]]:
        base_url = f'{self._url}/models'
        query_params = {}

        if model_name:
            return (
                f'{base_url}/{self._org}:{self._project_name}:{model_name}',
                query_params,
            )

        return base_url, {
            'organization_name': self._org,
            'project_name': self._project_name,
        }

    def _create_model_dict(
        self,
        name: str,
        id: int,
        info: dict = None,
        file_list: list = None,
        model_type: str = '',
        framework: str = '',
        requirements: str = '',
    ) -> dict:
        return {
            'id': id,
            'name': name,
            'info': info or {},
            'file_list': file_list or [],
            'model_type': model_type,
            'framework': framework,
            'requirements': requirements,
            'organization_name': self._org,
            'project_name': self._project_name,
        }

    def test_get_models(self):
        model_names = ['model_1', 'model_2', 'model_3']
        response_body = get_base_paginated_api_response_body(
            [
                self._create_model_dict(
                    name=name,
                    id=i,
                    info=self._example_model_info_dict,
                    file_list=self._example_file_list_dict,
                )
                for i, name in enumerate(model_names)
            ]
        )

        url, query_params = self._get_url_query_params()
        self.requests_mock.get(
            url, json=response_body, match=[matchers.query_param_matcher(query_params)]
        )

        models = self.client.get_models(project_id=self._project_name)
        self.assertTrue(isinstance(models, list))
        self.assertIsInstance(models[0], Model)
        self.assertEqual(models[0].name, model_names[0])
        self.assertEqual(models[1].name, model_names[1])
        self.assertEqual(models[2].name, model_names[2])
        self.assertDictEqual(models[0].info, self._example_model_info_dict)
        self.assertListEqual(models[0].file_list, self._example_file_list_dict)
        self.assertTrue(hasattr(models[0], 'name'))
        self.assertTrue(hasattr(models[0], 'id'))
        self.assertTrue(hasattr(models[0], 'info'))
        self.assertTrue(hasattr(models[0], 'file_list'))
        self.assertTrue(hasattr(models[0], 'model_type'))
        self.assertTrue(hasattr(models[0], 'framework'))
        self.assertTrue(hasattr(models[0], 'requirements'))

    def test_get_models_empty_list(self):
        model_names = []
        response_body = get_base_paginated_api_response_body(
            [
                self._create_model_dict(name=name, id=i)
                for i, name in enumerate(model_names)
            ]
        )

        url, _ = self._get_url_query_params()

        self.requests_mock.get(url, json=response_body)

        models = self.client.get_models(project_id=self._project_name)
        self.assertListEqual(models, model_names)
        self.assertTrue(isinstance(models, list))

    def _get_api_response_json(self, model: dict):
        response = get_base_api_response_body(data=model)
        return response

    def test_get_model(self):
        id = 0
        model_type = 'classification'
        framework = 'tensorflow'
        requirements = None

        response = self._get_api_response_json(
            self._create_model_dict(
                id=id,
                name=self._model_name,
                info=self._example_model_info_dict,
                file_list=self._example_file_list_dict,
                model_type=model_type,
                framework=framework,
                requirements=requirements,
            )
        )
        url, _ = self._get_url_query_params(model_name=self._model_name)

        self.requests_mock.get(url, json=response)

        model = self.client.get_model(
            project_id=self._project_name, model_id=self._model_name
        )

        self.assertIsInstance(model, Model)
        self.assertEqual(model.name, self._model_name)
        self.assertDictEqual(model.info, self._example_model_info_dict)
        self.assertListEqual(model.file_list, self._example_file_list_dict)
        self.assertEqual(model.id, id)
        self.assertEqual(model.model_type, model_type)
        self.assertEqual(model.framework, framework)
        self.assertEqual(model.requirements, requirements)

    def test_get_model_404(self):
        url, _ = self._get_url_query_params(model_name=self._model_name)
        self.requests_mock.get(
            url, json=get_404_error_response(), status=HTTPStatus.NOT_FOUND
        )

        with self.assertRaises(NotFound) as e:  # noqa
            _ = self.client.get_model(
                project_id=self._project_name, model_id=self._model_name
            )

    def test_delete_model(self):
        url, _ = self._get_url_query_params(self._model_name)

        self.requests_mock.delete(url)

        response = self.client.delete_model(
            model_id=self._model_name, project_id=self._project_name
        )

        self.assertIsNone(response)
