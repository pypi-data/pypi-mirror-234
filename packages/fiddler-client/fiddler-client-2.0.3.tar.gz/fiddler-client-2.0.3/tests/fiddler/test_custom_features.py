import pytest
from pydantic import ValidationError

from fiddler.schemas.custom_features import (
    CustomFeature,
    ImageEmbedding,
    Multivariate,
    TextEmbedding,
)


def test_custom_feature_from_dict():
    # Test 1: Correct input for Multivariate type
    result = CustomFeature.from_dict(
        {
            'name': 'test',
            'type': 'FROM_COLUMNS',
            'n_clusters': 5,
            'centroids': None,
            'columns': ['col1', 'col2'],
            'monitor_components': False,
        }
    )
    assert isinstance(result, Multivariate)

    # Test 2: Correct input for TextEmbedding type
    result = CustomFeature.from_dict(
        {
            'name': 'test',
            'type': 'FROM_TEXT_EMBEDDING',
            'source_column': 'col1',
            'column': 'col2',
        }
    )
    assert isinstance(result, TextEmbedding)

    # Test 3: Correct input for ImageEmbedding type
    result = CustomFeature.from_dict(
        {
            'name': 'test',
            'type': 'FROM_IMAGE_EMBEDDING',
            'source_column': 'col1',
            'column': 'col2',
        }
    )
    assert isinstance(result, ImageEmbedding)

    # Test 4: Incorrect input for Multivariate type (missing columns)
    with pytest.raises(ValidationError):
        result = CustomFeature.from_dict(
            {
                'name': 'test',
                'type': 'FROM_COLUMNS',
                'n_clusters': 5,
                'centroids': None,
                'monitor_components': False,
            }
        )

    # Test 5: Incorrect input for Embedding type (missing column)
    with pytest.raises(ValidationError):
        result = CustomFeature.from_dict(
            {
                'name': 'test',
                'type': 'FROM_TEXT_EMBEDDING',
                'source_column': 'col1',
            }
        )

    # Test 6: Unsupported type
    with pytest.raises(ValueError):
        result = CustomFeature.from_dict(
            {
                'name': 'test',
                'type': 'UNSUPPORTED_TYPE',
            }
        )

    # Test 7: Missing type
    with pytest.raises(KeyError):
        result = CustomFeature.from_dict(
            {
                'name': 'test',
            }
        )

    # Test 8: Missing name
    with pytest.raises(ValidationError):
        result = CustomFeature.from_dict(
            {
                'type': 'FROM_COLUMNS',
                'n_clusters': 5,
                'centroids': None,
                'columns': ['col1', 'col2'],
                'monitor_components': False,
            }
        )

    # Test 9: Invalid n_clusters (string instead of integer)
    with pytest.raises(ValidationError):
        result = CustomFeature.from_dict(
            {
                'name': 'test',
                'type': 'FROM_COLUMNS',
                'n_clusters': 'five',
                'centroids': None,
                'columns': ['col1', 'col2'],
                'monitor_components': False,
            }
        )
