from pathlib import Path
from typing import Dict

import pandas as pd

from fiddler.constants import FileType
from fiddler.core_objects import DatasetInfo
from fiddler.utils.helpers import map_extension_to_file_type
from fiddler.utils.logger import get_logger

LOG = get_logger(__name__)

NUM_ROWS = 1
JUST_THE_HEADER = 0


def validate_dataset_info(info: DatasetInfo) -> None:
    if not isinstance(info, DatasetInfo):
        raise ValueError(
            'Parameter `info` must be of type `DatasetInfo`. '
            f'Instead found object of type {type(info)}.'
        )


def validate_dataset_shape(files: Dict[str, Path]) -> None:
    rows = 0
    columns = 0

    for _, file_path in files.items():
        try:
            file_type = map_extension_to_file_type(file_path)
            if file_type == FileType.CSV:
                df = pd.read_csv(file_path, nrows=NUM_ROWS)
            elif file_type == FileType.PARQUET:
                df = pd.read_parquet(file_path)
            rows, columns = df.shape
        except pd.errors.EmptyDataError:
            rows = 0
            columns = 0

        # empty checks.
        if columns == 0:
            raise ValueError('No columns found in dataset provided.')
        if rows == 0:
            raise ValueError('No rows found in dataset provided.')


def validate_dataset_columns(dataset_info: DatasetInfo, file_path: Path) -> None:
    file_type = map_extension_to_file_type(file_path)
    if file_type == FileType.CSV:
        df = pd.read_csv(file_path, nrows=JUST_THE_HEADER)
    elif file_type == FileType.PARQUET:
        df = pd.read_parquet(file_path)

    missing_cols = set(col.name for col in dataset_info.columns) - set(
        df.columns.str.strip()
    )
    if len(missing_cols) > 0:
        LOG.warning(
            'Following columns are missing from uploaded dataset, '
            f'but are present in DatasetInfo schema: {missing_cols}.'
        )
