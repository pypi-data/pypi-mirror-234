import tempfile

import pandas as pd
import pytest
from pytest_mock import MockerFixture

from fiddler.api.generate_schema_mixin import SchemaGeneratorFactory
from tests.utils import MockResponse

test_df = df = pd.DataFrame(
    [
        {'col1': 1, 'col2': 'foo'},
        {'col1': 2, 'col2': 'bar'},
        {'col1': 3, 'col2': 'baz'},
    ]
)

test_api_response = {
    'data': {
        'schema_version': 1,
        'columns': [
            {
                'id': 'col1',
                'name': 'col1',
                'data_type': 'int',
                'min': 1,
                'max': 3,
                'bins': [
                    1.0,
                    1.2,
                    1.4,
                    1.6,
                    1.8,
                    2.0,
                    2.2,
                    2.4000000000000004,
                    2.6,
                    2.8,
                    3.0,
                ],
            },
            {
                'id': 'col2',
                'name': 'col2',
                'data_type': 'category',
                'categories': ['bar', 'baz', 'foo'],
            },
        ],
    }
}


@pytest.fixture
def mock_client(mocker: MockerFixture):
    mock_client = mocker.MagicMock()
    mock_client.post.return_value = MockResponse(test_api_response)
    yield mock_client


def test_infer_schema_with_dataframe(mock_client) -> None:
    schema_generator = SchemaGeneratorFactory.create(
        source=test_df,
    )

    schema_generator.generate(client=mock_client)

    assert len(mock_client.post.call_args.kwargs['data']['rows']) == test_df.shape[0]
    assert 'max_cardinality' not in mock_client.post.call_args.kwargs['data']


def test_infer_schema_with_max_cardinality(mock_client) -> None:
    schema_generator = SchemaGeneratorFactory.create(source=test_df, max_cardinality=10)

    schema_generator.generate(client=mock_client)

    assert len(mock_client.post.call_args.kwargs['data']['rows']) == test_df.shape[0]
    assert mock_client.post.call_args.kwargs['data']['max_cardinality'] == 10


def test_infer_schema_with_csv_file(mock_client) -> None:
    with tempfile.NamedTemporaryFile(suffix='.csv', mode='w') as temp_file:
        test_df.to_csv(temp_file.name, index=False)

        schema_generator = SchemaGeneratorFactory.create(
            source=temp_file.name,
        )

        schema_generator.generate(client=mock_client)

    assert len(mock_client.post.call_args.kwargs['data']['rows']) == test_df.shape[0]


def test_infer_schema_with_parquet_file(mock_client) -> None:
    with tempfile.NamedTemporaryFile(suffix='.parquet', mode='wb') as temp_file:
        test_df.to_parquet(temp_file.name, index=False)

        schema_generator = SchemaGeneratorFactory.create(
            source=temp_file.name,
        )

        schema_generator.generate(client=mock_client)

    assert len(mock_client.post.call_args.kwargs['data']['rows']) == test_df.shape[0]


def test_infer_schema_with_rows(mock_client) -> None:
    schema_generator = SchemaGeneratorFactory.create(
        source=test_df.to_dict(orient='records'),
    )

    schema_generator.generate(client=mock_client)

    assert len(mock_client.post.call_args.kwargs['data']['rows']) == test_df.shape[0]
