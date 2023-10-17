from unittest import mock

import pytest

import fiddler as fdl
from fiddler import FiddlerClient
from fiddler.core_objects import DatasetInfo, ModelInfo
from fiddler.schema.dataset import Dataset

model_info_json = {
    'model': {
        'name': 'dummy_model',
        'input-type': fdl.ModelInputType.TABULAR,
        'model-task': fdl.ModelTask.BINARY_CLASSIFICATION,
        'inputs': [
            {'column-name': 'input1_num', 'data-type': 'float', 'is-nullable': False},
        ],
        'outputs': [
            {'column-name': 'output1_num', 'data-type': 'float', 'is-nullable': False},
        ],
        'targets': [
            {
                'column-name': 'target_str',
                'data-type': 'category',
                'is-nullable': False,
                'possible-values': [True, False],
            },
        ],
        'target-class-order': [False, True],
    }
}

dataset_json = {
    'name': 'some_name',
    'columns': [
        {
            'column-name': 'input1_num',
            'data-type': 'float',
            'is-nullable': False,
            'value-range-min': 0,
            'value-range-max': 1.0,
        },
        {
            'column-name': 'output1_num',
            'data-type': 'float',
            'is-nullable': False,
            'value-range-min': -1,
            'value-range-max': 1,
        },
        {
            'column-name': 'target_str',
            'data-type': 'category',
            'possible-values': [True, False],
            'is-nullable': False,
        },
    ],
}


@mock.patch('fiddler.FiddlerClient')
def test_add_model_datasets_added(mock_client_v2):
    dataset_info = DatasetInfo.from_dict(dataset_json)
    dataset = Dataset(
        id=1,
        name='dataset_id_1',
        version='1',
        file_list={},
        info=dataset_info,
        organization_name='test_org',
        project_name='test_project',
    )
    mock_client_v2.get_dataset.return_value = dataset
    model_info: ModelInfo = fdl.ModelInfo.from_dict(model_info_json)

    assert model_info.datasets is None

    mock_client_v2.add_model(
        project_id='pid',
        model_id='mid',
        dataset_id='dataset_id_1',
        model_info=model_info,
    )


def test_add_model_invalid_model_info_v2_client():
    with pytest.raises(Exception):
        server_info_mock = mock.patch.object(FiddlerClient, '_get_server_info')
        server_info_mock.start()
        _check_semver_mock = mock.patch.object(FiddlerClient, '_check_server_version')
        _check_semver_mock.start()
        _check_vc_mock = mock.patch.object(
            FiddlerClient, '_check_version_compatibility'
        )
        _check_vc_mock.start()
        client = FiddlerClient('https://test_org.fiddler.ai', 'test_org', 'test_token')
        client.add_model(
            project_id='project1',
            model_id='model1',
            dataset_id='dataset_id_1',
            model_info='string_instead_of_model_info_object',
        )


def test_add_model_none_model_info_v2_client():
    with pytest.raises(ValueError) as cx:
        server_info_mock = mock.patch.object(FiddlerClient, '_get_server_info')
        server_info_mock.start()
        _check_semver_mock = mock.patch.object(FiddlerClient, '_check_server_version')
        _check_semver_mock.start()
        _check_vc_mock = mock.patch.object(
            FiddlerClient, '_check_version_compatibility'
        )
        _check_vc_mock.start()
        client = FiddlerClient('https://test_org.fiddler.ai', 'test_org', 'test_token')
        client.add_model(
            project_id='project1',
            model_id='model1',
            dataset_id='dataset_id_1',
            model_info=None,
        )

    assert cx.match('Please pass a valid ModelInfo object')
