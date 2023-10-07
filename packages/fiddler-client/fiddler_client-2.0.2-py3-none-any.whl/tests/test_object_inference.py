import numpy as np
import pandas as pd
import pytest

from fiddler.core_objects import DatasetInfo, DataType


def test_calculate_stats_for_col_empty_column():
    column_name = 'empty'
    column_series = pd.Series([np.nan, np.nan, np.nan])
    max_inferred_cardinality = 3
    data_type_version = 'v0'

    with pytest.raises(ValueError) as excinfo:
        DatasetInfo._calculate_stats_for_col(
            column_name, column_series, max_inferred_cardinality, data_type_version
        )

    assert (
        str(excinfo.value)
        == f'Column {column_name} is empty. Please remove it and re-upload the dataset.'
    )


def test_calculate_stats_for_col_object_dtype():
    column_name = 'object_dtype'
    column_series = pd.Series(['a', 'b', 'c', np.nan])
    max_inferred_cardinality = 3
    data_type_version = 'v0'
    result = DatasetInfo._calculate_stats_for_col(
        column_name, column_series, max_inferred_cardinality, data_type_version
    )

    assert result.data_type == DataType.CATEGORY
    assert result.name == 'object_dtype'
    assert result.possible_values == ['a', 'b', 'c']
    assert result.is_nullable == True


def test_calculate_stats_for_col_vector_dtype():
    column_name = 'vector_dtype'
    column_series = pd.Series(
        [np.array([1, 2, 3]), np.array([4, 5, 6]), np.array([7, 8, 9])]
    )
    max_inferred_cardinality = 3
    data_type_version = 'v0'
    result = DatasetInfo._calculate_stats_for_col(
        column_name, column_series, max_inferred_cardinality, data_type_version
    )

    assert result.data_type == DataType.VECTOR
    assert result.name == 'vector_dtype'
    assert result.possible_values == None
    assert result.is_nullable == False
    assert result.n_dimensions == 3


def test_calculate_stats_for_col_float_list():
    column_name = 'vector_dtype'
    column_series = pd.Series([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    max_inferred_cardinality = 3
    data_type_version = 'v0'
    result = DatasetInfo._calculate_stats_for_col(
        column_name, column_series, max_inferred_cardinality, data_type_version
    )

    assert result.data_type == DataType.VECTOR
    assert result.name == 'vector_dtype'
    assert result.possible_values == None
    assert result.is_nullable == False
    assert result.n_dimensions == 3


def test_calculate_stats_for_col_float_list_unequal():
    column_name = 'vector_dtype'
    column_series = pd.Series(
        [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0, 10, 11, 12]]
    )
    max_inferred_cardinality = 3
    data_type_version = 'v0'
    result = DatasetInfo._calculate_stats_for_col(
        column_name, column_series, max_inferred_cardinality, data_type_version
    )

    assert result.data_type == DataType.VECTOR
    assert result.name == 'vector_dtype'
    assert result.possible_values == None
    assert result.is_nullable == False
    assert result.n_dimensions == 3


def test_calculate_stats_for_col_string_list():
    column_name = 'vector_dtype'
    column_series = pd.Series([['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']])
    max_inferred_cardinality = 3
    data_type_version = 'v0'
    result = DatasetInfo._calculate_stats_for_col(
        column_name, column_series, max_inferred_cardinality, data_type_version
    )

    assert result.data_type == DataType.STRING
    assert result.name == 'vector_dtype'
    assert result.possible_values == None
    assert result.is_nullable == False


def test_calculate_stats_for_col_str():
    column_name = 'str_dtype'
    column_series = pd.Series(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'])
    max_inferred_cardinality = 2
    data_type_version = 'v0'
    result = DatasetInfo._calculate_stats_for_col(
        column_name, column_series, max_inferred_cardinality, data_type_version
    )

    assert result.data_type == DataType.STRING
    assert result.name == 'str_dtype'
    assert result.possible_values == None
    assert result.is_nullable == False


def test_calculate_stats_for_col_cat():
    column_name = 'cat_dtype'
    column_series = pd.Series(['a', 'b', 'c', 'd'])
    max_inferred_cardinality = 5
    data_type_version = 'v0'
    result = DatasetInfo._calculate_stats_for_col(
        column_name, column_series, max_inferred_cardinality, data_type_version
    )

    assert result.data_type == DataType.CATEGORY
    assert result.name == 'cat_dtype'
    assert result.possible_values == ['a', 'b', 'c', 'd']
    assert result.is_nullable == False


def test_from_datasetinfo_from_dataframe():
    df = pd.DataFrame(
        {
            'a': [1, 2, 3],
            'b': ['a', 'b', 'c'],
            'c': [np.array([1, 2, 3]), np.array([4, 5, 6]), np.array([7, 8, 9])],
            'd': [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
            'e': [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']],
        }
    )

    dataset_info = DatasetInfo.from_dataframe(df)
    column_names = [col.name for col in dataset_info.columns]
    assert column_names == ['a', 'b', 'c', 'd', 'e']
    assert dataset_info.columns[0].data_type == DataType.INTEGER
    assert dataset_info.columns[1].data_type == DataType.CATEGORY
    assert dataset_info.columns[2].data_type == DataType.VECTOR
    assert dataset_info.columns[3].data_type == DataType.VECTOR
    assert dataset_info.columns[4].data_type == DataType.STRING
