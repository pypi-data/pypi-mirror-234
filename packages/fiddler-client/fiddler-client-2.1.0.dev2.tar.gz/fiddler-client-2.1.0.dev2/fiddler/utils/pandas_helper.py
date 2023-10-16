from datetime import datetime
from typing import Any, Dict, Optional, Union

import numpy as np
import pandas as pd

from fiddler import constants
from fiddler.utils.logger import get_logger

LOG = get_logger(__name__)
TIMESTAMP = 'TIMESTAMP'


def is_datetime(pandas_series: Any) -> bool:
    """
    Return true if Series contains all valid dates.
    """
    # if pandas_series contains valid timestamp series to_datetime will not
    # throw an exception, which means all rows has timestamp.
    try:
        # From 2.0 doc: passing `format='ISO8601'` if your strings are all ISO8601
        #               but not necessarily in exactly the same format;
        # For case when series contains ['2023-11-12 09:15:32.23', '2023-12-11']
        pd.to_datetime(pandas_series, format=constants.TIMESTAMP_FORMAT_2, errors='raise')
        return True
    except Exception:
        return False


def is_list(pandas_series: Any) -> bool:
    """
    Return true if Series contains all valid lists.
    """
    try:
        return pd.Series(pandas_series).apply(lambda x: isinstance(x, list)).all()
    except Exception:
        return False


def is_vector_value(x: Union[list, np.ndarray]) -> bool:
    """check if the input is a vector"""
    if isinstance(x, list):
        x = np.array(x)

    return isinstance(x, np.ndarray) and np.issubdtype(x.dtype, np.number)


def clean_df_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the dataframe types into serializable formats where needed. Currently
    works to:
    - Convert datetime to string

    TODO: Expand to all other datatypes
    """
    for ind, col_type in enumerate(df.dtypes):
        col = df.columns[ind]
        if col_type is not None and 'datetime64' in str(col_type):
            # Skipping timezone information from the column.
            # REF: https://fiddlerlabs.atlassian.net/browse/FDL-2592
            df[col] = pd.to_datetime(df[col], utc=True).dt.tz_localize(None)
            df[col] = df[col].dt.strftime(constants.TIMESTAMP_FORMAT)
            df[col] = df[col].astype('string')

        # pandas considers the datatype as an object, if it finds multiple datatypes
        # in a column. If such columns are consists of timestamp values, and those
        # values are less than specified 'max_inferred_cardinality' value. System
        # infers the timestamp variable as a categorical variable. To avoid that,
        # we added a check where we check the object is a datetime object or not.
        # If yes, we convert the datetime object into string.
        elif col_type == object:
            if df[col].astype('string') is not None and is_datetime(
                df[col].astype('string')
            ):
                df[col] = pd.to_datetime(
                    df[col], format=constants.TIMESTAMP_FORMAT_2, utc=True
                ).dt.tz_localize(None)
                df[col] = df[col].astype('string')
    return df


def try_series_retype(
    series: pd.Series, new_type: str
) -> Union[pd.DataFrame, pd.Series]:
    if new_type in ['unknown', 'str']:
        # Do not retype data
        return series

    try:
        return series.astype(new_type)
    except (TypeError, ValueError) as e:
        if new_type == 'int':
            LOG.warning(
                f'"{series.name}" cannot be loaded as int '
                f'(likely because it contains missing values, and '
                f'Pandas does not support NaN for ints). Loading '
                f'as float instead.'
            )
            return series.astype('float')
        elif new_type.upper() == TIMESTAMP:
            try:
                return series.apply(
                    lambda x: datetime.strptime(x, constants.TIMESTAMP_FORMAT)
                )
            # if timestamp str doesn't contain millisec.
            # @NOTE: This can be a makeshift fix.
            except ValueError:
                # @TODO: Should such cases be
                # 1. handled by client OR
                # 2. should server apped 00 ms if not present during ingestion OR
                # 3. should it break if timestamp format does not match while ingestion?
                return series.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        else:
            raise e


def df_size_exceeds(dataset: Dict[str, pd.DataFrame], max_len: int) -> bool:
    """
    Returns True if size of any of the dataframes exceeds max_len
    """
    for name, df in dataset.items():
        if df.shape[0] > max_len:
            return True
    return False


def convert_flat_csv_data_to_grouped(
    input_data: pd.DataFrame, group_by_col: str, output_path: Optional[str] = None
) -> pd.DataFrame:
    """
    :param input_data: The dataframe with flat data.
    :param group_by_col: The column to group the data by.
    :param output_path: Optional argument, the path to write the grouped data to.
           If not specified, data won't be written anywhere.
    :return grouped_df: dataframe in grouped format
    """
    grouped_df = input_data.groupby(by=group_by_col, sort=False)
    grouped_df = grouped_df.aggregate(lambda x: x.tolist())

    if output_path is not None:
        grouped_df.to_csv(output_path)

    return grouped_df.reset_index()
