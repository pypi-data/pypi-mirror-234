import math
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd
from pyarrow.parquet import ParquetFile

from fiddler.core_objects import DataType
from fiddler.libs.http_client import RequestClient
from fiddler.schemas.model_schema import Column, ModelSchema
from fiddler.utils.decorators import check_version, handle_api_error_response
from fiddler.utils.response_handler import APIResponseHandler


class GenerateSchemaMixin:
    client: RequestClient
    organization_name: str

    @check_version(version_expr='>=23.4.0')
    @handle_api_error_response
    def generate_schema(
        self,
        source: Union[pd.DataFrame, Path, List[Dict[str, Any]], str],
        max_cardinality: Optional[int] = None,
        sample_size: Optional[int] = None,
        enrich: bool = True,
    ) -> ModelSchema:
        """
        Generate model schema from the given data
        :param source: Data source - Dataframe or path to csv or parquet file.
        :param max_cardinality: Max cardinality to detect categorical columns
        :param sample_size: No. of samples to use for generating schema
        :param enrich: Enrich the model schema client side by scanning all data
        :return: Generated ModelSchema object
        """
        schema_generator = SchemaGeneratorFactory.create(
            source=source,
            max_cardinality=max_cardinality,
            sample_size=sample_size,
            enrich=enrich,
        )

        return schema_generator.generate(client=self.client)


class BaseSchemaGenerator(ABC):
    SAMPLE_SIZE = 10_000
    CHUNK_SIZE = 10_000
    BIN_SIZE = 10
    MAX_CARDINALITY = 1_000

    def __init__(
        self,
        source: Any,
        max_cardinality: Optional[int] = None,
        sample_size: Optional[int] = None,
        enrich: bool = True,
    ):
        self.source = source
        self.max_cardinality = max_cardinality
        self._sample_size = sample_size or self.SAMPLE_SIZE
        self._num_rows: Union[int, None] = None
        self.should_enrich = enrich

    @property
    def num_rows(self) -> int:
        """Num of rows present in source"""
        if self._num_rows is None:
            self._num_rows = self._get_num_rows()

        return self._num_rows

    @abstractmethod
    def _get_num_rows(self) -> int:
        """Return number of rows present in the source"""

    @property
    def sample_size(self) -> int:
        """Sample size should not be greater than num rows"""
        return min(self._sample_size, self.num_rows)

    @property
    def num_chunks(self) -> int:
        """Number of chunks based on chunk size"""
        return math.ceil(self.num_rows / self.CHUNK_SIZE)

    @property
    def sample_size_per_chunk(self) -> int:
        """Number of samples per chunk"""
        return math.ceil(self.sample_size / self.num_chunks)

    @abstractmethod
    def sample_rows(self) -> pd.DataFrame:
        """Data sample which will be used for generating schema"""

    def generate(self, client: RequestClient) -> ModelSchema:
        """Call backend for generating model schema"""
        request_body = {
            'rows': self.sample_rows(),
        }

        if self.max_cardinality is not None:
            request_body['max_cardinality'] = self.max_cardinality

        response = client.post(
            url='generate-schema',
            data=request_body,
        )

        data = APIResponseHandler(response).get_data()

        schema = ModelSchema(**data)

        if self.should_enrich:
            schema = self._enrich(schema=schema)

        return schema

    @abstractmethod
    def get_series(self, col_name: str) -> pd.Series:
        """Return pandas series for the given column"""

    def _enrich_numeric_column(self, series: pd.Series, column: Column) -> Column:
        """Enrich numeric column with min/max/bins"""
        if series.empty:
            return column

        if column.data_type == DataType.INTEGER:
            series = series.astype('int64')
            column.min = int(series.min())
            column.max = int(series.max())
        elif column.data_type == DataType.FLOAT:
            series = series.astype('float64')
            column.min = float(series.min())
            column.max = float(series.max())

        column.bins = np.linspace(
            start=column.min,  # type: ignore
            stop=column.max,  # type: ignore
            num=self.BIN_SIZE + 1,
        ).tolist()

        return column

    def _enrich_categorical_column(self, series: pd.Series, column: Column) -> Column:
        """
        Enrich categorical column with categories. Convert CATEGORICAL column to
        STRING if no of categories cross max cardinality.
        """
        if series.empty:
            return column

        categories = series.unique().tolist()
        max_cardinality = self.max_cardinality or self.MAX_CARDINALITY
        if len(categories) > max_cardinality:
            column.data_type = DataType.STRING
            column.categories = None
        else:
            column.categories = sorted(categories)

        return column

    def _enrich(
        self,
        schema: ModelSchema,
    ) -> ModelSchema:
        """Enrich schema if source has more data than sample size"""
        if self.num_rows <= self.sample_size:
            return schema

        for index, column in enumerate(schema.columns):
            series = self.get_series(col_name=column.name)
            if column.data_type in {DataType.INTEGER, DataType.FLOAT}:
                schema.columns[index] = self._enrich_numeric_column(
                    series=series, column=column
                )
            elif column.data_type in {DataType.CATEGORY, DataType.STRING}:
                schema.columns[index] = self._enrich_categorical_column(
                    series=series, column=column
                )

        return schema


class CSVSchemaGenerator(BaseSchemaGenerator):
    def __init__(self, source: Path, *args: Any, **kwargs: Any) -> None:
        super().__init__(source, *args, **kwargs)

    def _get_num_rows(self) -> int:
        # Num of rows excluding header
        return sum(1 for _ in open(self.source)) - 1

    def sample_rows(self) -> List[Dict]:
        df = pd.concat(
            [
                chunk.sample(self.sample_size_per_chunk)
                for chunk in pd.read_csv(
                    self.source, chunksize=self.CHUNK_SIZE, dtype='str'
                )
            ]
        )

        return df.to_dict(orient='records')

    def get_series(self, col_name: str) -> pd.Series:
        df = pd.read_csv(self.source, usecols=[col_name])
        return df[col_name]


class ParquetSchemaGenerator(BaseSchemaGenerator):
    def __init__(self, source: Path, *args: Any, **kwargs: Any) -> None:
        super().__init__(source, *args, **kwargs)

        self.parquet_file = ParquetFile(self.source)

    def _get_num_rows(self) -> int:
        return self.parquet_file.scan_contents(batch_size=self.CHUNK_SIZE)

    def sample_rows(self) -> List[Dict]:
        df = pd.concat(
            [
                batch.to_pandas().sample(self.sample_size_per_chunk)
                for batch in self.parquet_file.iter_batches()
            ]
        )
        return df.astype('str').to_dict(orient='records')

    def get_series(self, col_name: str) -> pd.Series:
        df = pd.read_parquet(self.source, columns=[col_name])
        return df[col_name]


class DataframeSchemaGenerator(BaseSchemaGenerator):
    def __init__(self, source: pd.DataFrame, *args: Any, **kwargs: Any) -> None:
        super().__init__(source, *args, **kwargs)

    def _get_num_rows(self) -> int:
        return self.source.shape[0]

    def sample_rows(self) -> List[Dict]:
        return (
            self.source.sample(self.sample_size).astype('str').to_dict(orient='records')
        )

    def get_series(self, col_name: str) -> pd.Series:
        return self.source[col_name]


class ListSchemaGenerator(BaseSchemaGenerator):
    def __init__(self, source: List[Dict[str, Any]], *args: Any, **kwargs: Any) -> None:
        super().__init__(source, *args, **kwargs)

    def _get_num_rows(self) -> int:
        return len(self.source)

    def sample_rows(self) -> List[Dict]:
        return self.source

    def enrich(
        self,
        schema: ModelSchema,
    ) -> ModelSchema:
        return schema

    def get_series(self, col_name: str) -> pd.Series:
        raise NotImplementedError


class SchemaGeneratorFactory:
    @staticmethod
    def create(
        source: Union[pd.DataFrame, Path, List[Dict[str, Any]], str],
        max_cardinality: Optional[int] = None,
        sample_size: Optional[int] = None,
        enrich: bool = False,
    ) -> BaseSchemaGenerator:
        schema_generator_class: Any = None
        if isinstance(source, pd.DataFrame):
            schema_generator_class = DataframeSchemaGenerator
        elif isinstance(source, (Path, str)):
            source = Path(source) if isinstance(source, str) else source
            if source.name.endswith('.csv'):
                schema_generator_class = CSVSchemaGenerator
            elif source.name.endswith('.parquet'):
                schema_generator_class = ParquetSchemaGenerator
        elif isinstance(source, list):
            schema_generator_class = ListSchemaGenerator

        if not schema_generator_class:
            raise ValueError(
                'Invalid source. Pass dataframe, path to csv/parquet file or list of '
                'rows instead'
            )

        return schema_generator_class(
            source=source,
            max_cardinality=max_cardinality,
            sample_size=sample_size,
            enrich=enrich,
        )
