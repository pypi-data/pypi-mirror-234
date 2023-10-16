# TODO: Add License
from __future__ import annotations

import copy
import enum
import functools
import json
import textwrap
import warnings
from dataclasses import asdict, dataclass
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
    cast,
)

import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype

from fiddler.schemas.custom_features import (
    CustomFeature,
    ImageEmbedding,
    TextEmbedding,
    VectorFeature,
)
from fiddler.utils.formatting import prettyprint_number, validate_sanitized_names
from fiddler.utils.logger import get_logger
from fiddler.utils.pandas_helper import is_datetime, is_list, is_vector_value

DEFAULT_MAX_INFERRED_CARDINALITY = 100
PD_TYPE_VECTOR = 'vector'

# default for DatasetInfo.data_type_version and ModelInfo.data_type_version
# Introduced to bypass certain data type conversion functions
# from both client and server.
# More details https://fiddlerlabs.atlassian.net/wiki/spaces/FL/pages/1973617158/Introducing+Version+in+DatasetInfo+and+ModelInfo

# v0 means variable is just defined, no change in any logic.
# v0 is launched in python-client release 1.7.0

# v1 ignores typecasting of possible_values of categorical data type
# v1 is launched in python-client release 2.0.0
CURRENT_DATA_TYPE_VERSION: str = 'v1'

LOG = get_logger(__name__)


class IntegrityViolationStatus(NamedTuple):
    is_nullable_violation: bool
    is_type_violation: bool
    is_range_violation: bool


class MonitoringViolation:
    """Object to track monitoring violations for pre-flight checks that can
    be trigerred via publish_event function with dry_run flag
    """

    def __init__(self, _type: str, desc: str) -> None:
        self.type = _type
        self.desc = desc


@enum.unique
class MonitoringViolationType(enum.Enum):
    """Fatal violations would cause monitoring to not work whereas warning violation
    can cause one or more monitoring features to not work.
    """

    FATAL = 'fatal'
    WARNING = 'warning'


@enum.unique
class HigherLevelAggregates(enum.Enum):
    """Supported Higher Level Aggregates"""

    TOP_K = 'top K'


@enum.unique
class FiddlerEventColumns(enum.Enum):
    OCCURRED_AT = '__occurred_at'
    MODEL = '__model'
    ORG = '__org'
    PROJECT = '__project'
    UPDATED_AT = '__updated_at'
    EVENT_ID = '__event_id'
    EVENT_TYPE = '__event_type'


@enum.unique
class EventTypes(enum.Enum):
    """We are mostly using execution and update events. Others are *probably* deprecated"""

    EXECUTION_EVENT = 'execution_event'
    UPDATE_EVENT = 'update_event'
    PREDICTION_EVENT = 'prediction_event'
    MODEL_ACTIVITY_EVENT = 'model_activity_event'
    MONITORING_CONFIG_UPDATE = 'monitoring_config_update'


class FiddlerPublishSchema:
    STATIC = '__static'
    DYNAMIC = '__dynamic'
    ITERATOR = '__iterator'
    UNASSIGNED = '__unassigned'
    HEADER_PRESENT = '__header_present'

    ORG = '__org'
    MODEL = '__model'
    PROJECT = '__project'
    TIMESTAMP = '__timestamp'
    DEFAULT_TIMESTAMP = '__default_timestamp'
    TIMESTAMP_FORMAT = '__timestamp_format'
    EVENT_ID = '__event_id'
    IS_UPDATE_EVENT = '__is_update_event'
    STATUS = '__status'
    LATENCY = '__latency'
    ITERATOR_KEY = '__iterator_key'

    CURRENT_TIME = 'CURRENT_TIME'


@enum.unique
class BatchPublishType(enum.Enum):
    """Supported Batch publish for the Fiddler engine."""

    DATAFRAME = 0
    LOCAL_DISK = 1
    AWS_S3 = 2
    GCP_STORAGE = 3


@enum.unique
class FiddlerTimestamp(enum.Enum):
    """Supported timestamp formats for events published to Fiddler"""

    EPOCH_MILLISECONDS = 'epoch milliseconds'
    EPOCH_SECONDS = 'epoch seconds'
    ISO_8601 = '%Y-%m-%d %H:%M:%S.%f'  # LOOKUP
    INFER = 'infer'


@enum.unique
class DataType(enum.Enum):
    """Supported datatypes for the Fiddler engine."""

    FLOAT = 'float'
    INTEGER = 'int'
    BOOLEAN = 'bool'
    STRING = 'str'
    CATEGORY = 'category'
    TIMESTAMP = 'timestamp'
    VECTOR = 'vector'

    def is_numeric(self) -> bool:
        return self.value in (DataType.INTEGER.value, DataType.FLOAT.value)

    def is_bool_or_cat(self) -> bool:
        return self.value in (DataType.BOOLEAN.value, DataType.CATEGORY.value)

    def is_valid_target(self) -> bool:
        return self.value != DataType.STRING.value

    def is_vector(self) -> bool:
        return self.value == DataType.VECTOR.value


@enum.unique
class ArtifactStatus(enum.Enum):
    """Artifact Status, default to USER_UPLOADED"""

    NO_MODEL = 'no_model'
    SURROGATE = 'surrogate'
    USER_UPLOADED = 'user_uploaded'


@enum.unique
class ExplanationMethod(enum.Enum):
    SHAP = 'shap'
    FIDDLER_SV = 'fiddler_shapley_values'
    IG = 'ig'
    IG_FLEX = 'ig_flex'
    MEAN_RESET = 'mean_reset'
    PERMUTE = 'permute'


BUILT_IN_EXPLANATION_NAMES = [method.value for method in ExplanationMethod]


@enum.unique
class ModelTask(enum.Enum):
    """Supported model tasks for the Fiddler engine."""

    BINARY_CLASSIFICATION = 'binary_classification'
    MULTICLASS_CLASSIFICATION = 'multiclass_classification'
    REGRESSION = 'regression'
    RANKING = 'ranking'
    NOT_SET = 'not_set'
    LLM = 'llm'

    def is_classification(self) -> bool:
        return self.value in (
            ModelTask.BINARY_CLASSIFICATION.value,
            ModelTask.MULTICLASS_CLASSIFICATION.value,
        )

    def is_regression(self) -> bool:
        return self.value in (ModelTask.REGRESSION.value)


@enum.unique
class BuiltInMetrics(enum.Enum):
    """Supported metrics for segments."""

    MAPE = 'MAPE'
    WMAPE = 'WMAPE'
    R2 = 'r2'
    MSE = 'mse'
    MAE = 'mae'
    LOG_LOSS = 'log_loss'
    ACCURACY = 'accuracy'
    PRECISION = 'precision'
    RECALL = 'recall'
    F1_SCORE = 'f1_score'
    AUC = 'auc'

    @classmethod
    def get_binary(cls) -> List['BuiltInMetrics']:
        'return binary classification metrics'
        return [
            BuiltInMetrics.ACCURACY,
            BuiltInMetrics.PRECISION,
            BuiltInMetrics.RECALL,
            BuiltInMetrics.F1_SCORE,
            BuiltInMetrics.AUC,
        ]

    @classmethod
    def get_multiclass(cls) -> List['BuiltInMetrics']:
        'return multiclass classification metrics'
        return [BuiltInMetrics.ACCURACY, BuiltInMetrics.LOG_LOSS]

    @classmethod
    def get_regression(cls) -> List['BuiltInMetrics']:
        'return regression metrics'
        return [
            BuiltInMetrics.R2,
            BuiltInMetrics.MSE,
            BuiltInMetrics.MAE,
            BuiltInMetrics.MAPE,
            BuiltInMetrics.WMAPE,
        ]


@enum.unique
class ModelInputType(enum.Enum):
    """Supported model paradigms for the Fiddler engine."""

    TABULAR = 'structured'
    TEXT = 'text'
    MIXED = 'mixed'


@enum.unique
class DeploymentType(str, enum.Enum):
    EXECUTOR = 'executor'
    NO_MODEL = 'no-model'
    PREDICTOR = 'predictor'
    SURROGATE = 'surrogate'


class AttributionExplanation(NamedTuple):
    """The results of an attribution explanation run by the Fiddler engine."""

    algorithm: str
    inputs: List[str]
    attributions: List[float]
    misc: Optional[dict]

    @classmethod
    def from_dict(cls, deserialized_json: dict) -> AttributionExplanation:
        """Converts a deserialized JSON format into an
        AttributionExplanation object"""

        algorithm = deserialized_json.pop('explanation_type')

        if 'GEM' in deserialized_json:
            return cls(
                algorithm=algorithm,
                inputs=[],
                attributions=deserialized_json.pop('GEM'),
                misc=deserialized_json,
            )

        else:
            if algorithm == 'ig' and deserialized_json['explanation'] == {}:
                input_attr = deserialized_json.pop('explanation_ig')
                inputs, attributions = input_attr[0], input_attr[1]
            else:
                inputs, attributions = zip(
                    *deserialized_json.pop('explanation').items()
                )

        return cls(
            algorithm=algorithm,
            inputs=list(inputs),
            attributions=list(attributions),
            misc=deserialized_json,
        )


class MulticlassAttributionExplanation(NamedTuple):
    """A collection of AttributionExplanation objects explaining several
    classes' predictions in a multiclass classification setting."""

    classes: Tuple[str]
    explanations: Dict[str, AttributionExplanation]

    @classmethod
    def from_dict(cls, deserialized_json: dict) -> MulticlassAttributionExplanation:
        """Converts a deserialized JSON format into an
        MulticlassAttributionExplanation object"""
        return cls(
            classes=cast(Tuple[str], tuple(deserialized_json.keys())),
            explanations={
                label_class: AttributionExplanation.from_dict(explanation_dict)
                for label_class, explanation_dict in deserialized_json.items()
            },
        )


class Column:
    """Represents a single column of a dataset or model input/output.

    :param name: The name of the column (corresponds to the header row of a
        CSV file)
    :param data_type: The best encoding type for this column's data.
    :param possible_values: If data_type is CATEGORY, then an exhaustive list
        of possible values for this category must be provided. Otherwise
        this field has no effect and is optional.
    :param is_nullable: Optional metadata. Tracks whether or not this column is
        expected to contain some null values.
    :param value_range_x: Optional metadata. If data_type is FLOAT or INTEGER,
        then these values specify a range this column's values are expected to
        stay within. Has no effect for non-numerical data_types.
    """

    def __init__(
        self,
        name: str,
        data_type: DataType,
        possible_values: Optional[List[Any]] = None,
        is_nullable: Optional[bool] = None,
        value_range_min: Optional[Union[int, float]] = None,
        value_range_max: Optional[Union[int, float]] = None,
        n_dimensions: Optional[int] = None,
    ):
        self.name = name
        self.data_type = data_type
        self.is_nullable = is_nullable

        self.possible_values = possible_values
        self.value_range_min = value_range_min
        self.value_range_max = value_range_max
        self.n_dimensions = n_dimensions

        inappropriate_value_range = not self.data_type.is_numeric() and not (
            self.value_range_min is None and self.value_range_max is None
        )
        if inappropriate_value_range:
            raise ValueError(
                f'Do not pass `value_range` for '
                f'non-numerical {self.data_type} data type.'
            )

    @classmethod
    def from_dict(cls, desrialized_json: dict) -> Column:
        """Creates a Column object from deserialized JSON"""
        return cls(
            name=desrialized_json['column-name'],
            data_type=DataType(desrialized_json['data-type']),
            possible_values=desrialized_json.get('possible-values', None),
            is_nullable=desrialized_json.get('is-nullable', None),
            value_range_min=desrialized_json.get('value-range-min', None),
            value_range_max=desrialized_json.get('value-range-max', None),
            n_dimensions=desrialized_json.get('n-dimensions', None),
        )

    def copy(self) -> Column:
        return copy.deepcopy(self)

    def __repr__(self) -> str:
        res = (
            f'Column(name="{self.name}", data_type={self.data_type}, '
            f'possible_values={self.possible_values}'
        )
        if self.is_nullable is not None:
            res += f', is_nullable={self.is_nullable}'
        if self.value_range_min is not None or self.value_range_max is not None:
            res += (
                f', value_range_min={self.value_range_min}'
                f', value_range_max={self.value_range_max}'
            )
        if self.n_dimensions is not None:
            res += f', n_dimensions={self.n_dimensions}'
        res += ')'
        return res

    def _raise_on_bad_categorical(self) -> None:
        """Raises a ValueError if data_type=CATEGORY without possible_values"""
        if (
            self.data_type.value == DataType.CATEGORY.value
            and self.possible_values is None
        ):
            # Commenting to allow none possible values
            self.possible_values = []
            # raise ValueError(
            #     f'Mal-formed categorical column missing `possible_values`: ' f'{self}'
            # )

    def get_pandas_dtype(self) -> CategoricalDtype | str:
        """Converts the data_type field to a Pandas-friendly form."""
        # Commenting to allow none possible values.
        # self._raise_on_bad_categorical()

        if self.data_type.value == DataType.CATEGORY.value:
            return CategoricalDtype(self.possible_values)
        return self.data_type.value

    def to_dict(self) -> Dict[str, Any]:
        """Converts this object to a more JSON-friendly form."""
        res: Dict[str, Any] = {
            'column-name': self.name,
            'data-type': self.data_type.value,
        }
        if self.possible_values is not None:
            # possible-values can be string, int, etc
            # no need to convert everything to str
            res['possible-values'] = [val for val in self.possible_values]
        if self.is_nullable is not None:
            res['is-nullable'] = self.is_nullable
        if self.value_range_min is not None:
            res['value-range-min'] = self.value_range_min
        if self.value_range_max is not None:
            res['value-range-max'] = self.value_range_max
        if self.n_dimensions is not None:
            res['n-dimensions'] = self.n_dimensions
        return res

    @staticmethod
    def _value_is_na_or_none(value: Union[None, str]) -> bool | pd.Series:
        if value is None:
            return True
        # This needs to be added because when we add `pandas._libs.missing.NAType` type in rabbitmq.
        # When we read the message, it converts the value to the "<NA>".
        if isinstance(value, str):
            return '<NA>' == value
        try:
            return pd.isnull(value)
        except TypeError:
            return False


def _get_field_pandas_dtypes(
    column_sequence: Sequence[Column],
) -> Dict[str, Union[str, CategoricalDtype]]:
    """Get a dictionary describing the pandas datatype of every column in a
    sequence of columns."""
    dtypes = dict()
    for column in column_sequence:
        dtypes[column.name] = column.get_pandas_dtype()
    return dtypes


@dataclass
class WeightingParams:
    """Holds weighting information for class imbalanced models

    :param class_weight: list of floats representing weights for each of the classes. The length
        must equal the no. of classes.
    :param weighted_reference_histograms: Flag indicating if baseline histograms must be weighted or not
        when calculating drift metrics.
    :param weighted_surrogate_training: Flag indicating if weighting scheme should be used when training the
        surrogate model.

    :return: A WeightingParams object
    """

    class_weight: Optional[List[float]] = None
    weighted_reference_histograms: bool = True
    weighted_surrogate_training: bool = True

    def __post_init__(self) -> None:
        # raise an error if neither both class and sample weighting is specified
        if self.class_weight is None:
            raise ValueError('Need to specify class_weights')
        if not isinstance(self.class_weight, List):
            raise ValueError(
                f'Expected class_weight to be a list of floats instead received {type(self.class_weight)}'
            )
        try:
            self.class_weight = [round(float(w), 4) for w in self.class_weight]
            # validate class-weights
            for wt in self.class_weight:
                if wt < 0:
                    raise ValueError('Class-weights cannot be negative.')
        except ValueError:
            raise ValueError('Expected class_weight to be a list of floats')
        return

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Any) -> WeightingParams:
        return cls(**d)


class DatasetInfo:

    """Information about a dataset. Defines the schema.

    :param display_name: A name for user-facing display (different from an id).
    :param columns: A list of Column objects.
    :param files: Optional. If the dataset is stored in one or more CSV files
        with canonical names, this field lists those files. Primarily for use
        only internally to the Fiddler engine.
    :param data_type_version: [Optional] a String indicating CURRENT_DATA_TYPE_VERSION.
        Used mainly for data type conversion rules for possible_values.
    """

    def __init__(
        self,
        display_name: str,
        columns: List[Column],
        files: Optional[List[str]] = None,
        dataset_id: Optional[str] = None,
        data_type_version: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        self.display_name = display_name
        self.dataset_id = dataset_id
        self.columns = DatasetInfo._datatype_check(columns)
        self.files = files if files is not None else list()
        self.data_type_version = data_type_version
        self.misc = kwargs

    def get_pandas_dtypes(self) -> Dict:
        """
        Convert dataset info columns data types to pandas compatible data types
        :return: Dictionary of pandas data types for dataset columns
        """

        dtypes = {}

        for column in self.columns:
            dtypes[column.name] = column.get_pandas_dtype()

        return dtypes

    def get_column_names(self) -> List[str]:
        """Returns a list of column names."""
        return [column.name for column in self.columns]

    def get_column_pandas_dtypes(
        self,
    ) -> Dict[str, Union[str, CategoricalDtype]]:
        """Get a dictionary describing the pandas datatype of every column."""
        return _get_field_pandas_dtypes(self.columns)

    @staticmethod
    def _datatype_check(columns: List[Any]) -> List:
        """
        # loop through all columns
        # if the column datatype is numpy datatype, transform to python type
        """
        for column in columns:
            column.value_range_max = DatasetInfo._transform_type(column.value_range_max)
            column.value_range_min = DatasetInfo._transform_type(column.value_range_min)
        return columns

    @staticmethod
    def _transform_type(val: Any) -> Union[float, int, bool]:
        if isinstance(val, np.bool_):
            val = bool(val)
        if isinstance(val, np.integer):
            val = int(val)
        if isinstance(val, np.floating):
            val = float(val)
        return val

    @staticmethod
    def datatype_from_pandas_dtype(pd_dtype: Any) -> DataType:
        if pd.api.types.is_float_dtype(pd_dtype):
            return DataType.FLOAT
        if pd.api.types.is_integer_dtype(pd_dtype):
            return DataType.INTEGER
        if pd.api.types.is_bool_dtype(pd_dtype):
            return DataType.BOOLEAN
        if pd.api.types.is_categorical_dtype(pd_dtype):
            return DataType.CATEGORY
        if pd_dtype == PD_TYPE_VECTOR:
            return DataType.VECTOR

        return DataType.STRING

    @classmethod
    def update_stats_for_existing_schema(
        cls, dataset: dict, info: Any, max_inferred_cardinality: Optional[int] = None
    ) -> DatasetInfo:
        """Takes a customer/user provided schema along with a bunch
        of files with corresponding data in dataframes and merges them
        together and updates the user schema.
        Please note that we DO NOT update stats in the user provided
        schema if those stats are already there. We assume that the
        user wants those stats for data integrity testing.
        """
        updated_infos = []
        for name, item in dataset.items():
            update_info = DatasetInfo.check_and_update_column_info(
                info, item, max_inferred_cardinality
            )
            updated_infos.append(update_info)
        info = DatasetInfo.as_combination(
            updated_infos,
            display_name=info.display_name,
        )
        return info

    @classmethod
    def check_and_update_column_info(
        cls,
        info_original: Any,
        df: pd.DataFrame,
        max_inferred_cardinality: Optional[int] = None,
    ) -> DatasetInfo:
        """When called on a Dataset, this function will calculate stats
        that are used by DI and put add them to each Column in case its
        not already there. Currently stats include is_nullable, possible_values, and
        min/max ranges.
        Please note that we DO NOT update stats in the user provided
        schema if those stats are already there. We assume that the
        user wants those stats for data integrity testing.
        """

        info = copy.deepcopy(info_original)
        if df.index.name is not None:
            # add index column if it is not just an unnamed RangeIndex
            df = df.reset_index(inplace=False)
        name_series_iter = df.items()
        column_stats = {}
        for column_name, column_series in name_series_iter:
            column_info = cls._calculate_stats_for_col(
                column_name, column_series, max_inferred_cardinality
            )
            column_stats[column_name] = column_info

        for column in info.columns:
            # Fill in stats for each column if its not present
            column_info = column_stats[column.name]
            if not column.is_nullable:
                column.is_nullable = column_info.is_nullable
            if not column.value_range_min:
                column.value_range_min = column_info.value_range_min
            if not column.value_range_max:
                column.value_range_max = column_info.value_range_max
            if not column.possible_values:
                column.possible_values = column_info.possible_values

        return cls(
            info.display_name, info.columns, data_type_version=CURRENT_DATA_TYPE_VERSION
        )

    @classmethod
    def from_dataframe(
        cls,
        df: Union[pd.DataFrame, Iterable[pd.DataFrame]],
        display_name: str = '',
        max_inferred_cardinality: Optional[int] = DEFAULT_MAX_INFERRED_CARDINALITY,
        dataset_id: Optional[str] = None,
    ) -> DatasetInfo:
        """Infers a DatasetInfo object from a pandas DataFrame
        (or iterable of DataFrames).

        :param df: Either a single DataFrame or an iterable of DataFrame
            objects. If an iterable is given, all dataframes must have the
            same columns.
        :param display_name: A name for user-facing display (different from
            an id).
        :param max_inferred_cardinality: Optional. If not None, any
            string-typed column with fewer than `max_inferred_cardinality`
            unique values will be inferred as a category (useful for cases
            where use of the built-in CategoricalDtype functionality of Pandas
            is not desired). Defaults to 100.
        :param dataset_id: Optionally specify the dataset_id.

        :returns: A DatasetInfo object.
        """
        # if an iterable is passed, infer for each in the iterable and combine
        if not isinstance(df, pd.DataFrame):
            info_gen = (
                cls.from_dataframe(
                    item, max_inferred_cardinality=max_inferred_cardinality
                )
                for item in df
            )
            return cls.as_combination(info_gen, display_name=display_name)

        columns = []
        if df.index.name is not None:
            # add index column if it is not just an unnamed RangeIndex
            df = df.reset_index(inplace=False)
        name_series_iter = df.items()
        for column_name, column_series in name_series_iter:
            column_info = cls._calculate_stats_for_col(
                column_name,
                column_series,
                max_inferred_cardinality,
                data_type_version=CURRENT_DATA_TYPE_VERSION,
            )
            columns.append(column_info)
        return cls(
            display_name,
            columns,
            dataset_id=dataset_id,
            data_type_version=CURRENT_DATA_TYPE_VERSION,
        )

    @staticmethod
    def _calculate_stats_for_col(
        column_name: str,
        column_series: pd.DataFrame,
        max_inferred_cardinality: Any,
        data_type_version: Optional[str] = 'v0',
    ) -> Column:
        # @TODO Automatically drop the empty column with warning and proceed instead of aborting the upload
        if column_series.isna().all():
            raise ValueError(
                f'Column {column_name} is empty. '
                f'Please remove it and re-upload the dataset.'
            )

        # if we infer string or categorical, ensure that the underlying data
        # is also string by casting it.

        # FDL-10905: dropna is needed to take care of cases where having None changes
        # data type of int, float, bool to category. dropna() won't change
        # is_nullable detection as column_series.dropna() returns a new instance.

        column_series_dropped_na = column_series.dropna()
        pd_column_dtype = column_series_dropped_na.infer_objects().dtype
        if pd.api.types.is_object_dtype(pd_column_dtype):
            row_count = column_series_dropped_na.shape[0]
            if row_count > 0 and is_vector_value(column_series_dropped_na[0]):
                iteration_count = min(row_count, 100)

                for i in range(iteration_count):
                    if not is_vector_value(column_series_dropped_na[i]):
                        break

                if i == iteration_count - 1:
                    pd_column_dtype = PD_TYPE_VECTOR

        column_dtype = DatasetInfo.datatype_from_pandas_dtype(pd_column_dtype)
        # get nullability before any datatype modifications like 'astype'
        # which distorts None values.
        is_nullable = bool(column_series.isna().any())

        if column_dtype in [DataType.CATEGORY, DataType.STRING]:
            if 'mixed' in pd.api.types.infer_dtype(column_series):
                LOG.warning(
                    '***********************************\n'
                    'WARNING: The column passed has mixed datatypes.\n'
                    ' We have casted the column to string to ensure smooth functionality.\n'
                    '***********************************'
                )

        # infer categorical if configured to do so
        if (
            max_inferred_cardinality
            and column_dtype.value == DataType.STRING.value
            and not is_datetime(column_series)
            and not is_list(column_series)
            and column_series_dropped_na.nunique() <= max_inferred_cardinality
        ):
            column_dtype = DataType.CATEGORY

        # get possible values for categorical type
        if column_dtype.is_bool_or_cat():
            # Only when data_type_version is 'v0',
            # categorical column values undergo int/bool -> float -> string conversion.
            if data_type_version == 'v0':
                possible_values = np.sort(
                    column_series_dropped_na.astype(str).unique()
                ).tolist()
                possible_values_floats = None
                if column_dtype.value == DataType.CATEGORY.value:
                    try:
                        possible_values_floats = [
                            str(float(raw_val)) for raw_val in possible_values
                        ]
                    except ValueError:
                        pass
                if possible_values_floats is not None:
                    possible_values = possible_values_floats
            else:
                possible_values = np.sort(column_series_dropped_na.unique()).tolist()
        else:
            possible_values = None

        # get value range for numerical dtype
        if column_dtype.is_numeric():
            # these are saved as series members.
            value_min, value_max = column_series.min(), column_series.max()
            if np.isnan(value_min):
                value_min = None
            if np.isnan(value_max):
                value_max = None
        else:
            value_min, value_max = None, None

        # get n_dimensions for vector dtype
        if column_dtype == DataType.VECTOR:
            # pick the most common length of the vector
            n_dimensions = int(column_series_dropped_na.apply(len).mode()[0])
        else:
            n_dimensions = None

        return Column(
            name=column_name,
            data_type=column_dtype,
            possible_values=possible_values,
            is_nullable=is_nullable,
            value_range_min=value_min,
            value_range_max=value_max,
            n_dimensions=n_dimensions,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Converts this object to a more JSON-friendly form."""
        res = {
            'name': self.display_name,
            'data_type_version': self.data_type_version,
            'columns': [c.to_dict() for c in self.columns],
            'files': self.files,
        }
        return {**res, **self.misc}

    @classmethod
    def from_dict(cls, deserialized_json: dict) -> DatasetInfo:
        """Transforms deserialized JSON into a DatasetInfo object"""
        # drop down into the "dataset" object inside the deserialized_json
        if 'dataset' in deserialized_json:
            deserialized_json = deserialized_json['dataset']
        if 'chunked_sources' in deserialized_json:
            return cls(
                display_name=deserialized_json['name'],
                columns=[Column.from_dict(c) for c in deserialized_json['columns']],
                files=deserialized_json.get('files', None),
                data_type_version=deserialized_json.get('data_type_version', None),
                misc={
                    'chunked_sources': deserialized_json.get('chunked_sources', None)
                },
            )
        # instantiate the class
        return cls(
            display_name=deserialized_json['name'],
            columns=[Column.from_dict(c) for c in deserialized_json['columns']],
            files=deserialized_json.get('files', None),
            data_type_version=deserialized_json.get('data_type_version', None),
        )

    @classmethod
    def _combine(
        cls, info_a: DatasetInfo, info_b: DatasetInfo, display_name: str = ''
    ) -> DatasetInfo:
        """Given two DatasetInfo objects, tries to combine them into
        a single DatasetInfo that describes both sub-datasets."""
        # raise error if column names are incompatible
        if info_a.get_column_names() != info_b.get_column_names():
            raise ValueError(
                f'Incompatible DatasetInfo objects: column names do not '
                f'match:\n{info_a.get_column_names()}\n'
                f'{info_b.get_column_names()}'
            )

        # combine columns
        columns = list()
        for a_column, b_column in zip(info_a.columns, info_b.columns):
            # resolve types
            a_type, b_type = a_column.data_type.value, b_column.data_type.value
            if a_type == b_type:
                col_type = a_column.data_type
            elif {a_type, b_type}.issubset(
                {DataType.BOOLEAN.value, DataType.INTEGER.value}
            ):
                col_type = DataType.INTEGER
            elif {a_type, b_type}.issubset(
                {DataType.BOOLEAN.value, DataType.INTEGER.value, DataType.FLOAT.value}
            ):
                col_type = DataType.FLOAT
            else:
                col_type = DataType.STRING

            # resolve possible_values
            if col_type.value == DataType.CATEGORY.value:
                assert a_column.possible_values is not None  # nosec
                assert b_column.possible_values is not None  # nosec
                # Merging the unique possible values after removing the None values.
                possible_values: Optional[List[Any]] = list(
                    set(list(filter(None, a_column.possible_values)))
                    or set(list(filter(None, b_column.possible_values)))
                )
                # Sort the final list to make sure the order is consistent.
                if possible_values and len(possible_values) > 0:
                    possible_values.sort()
            else:
                possible_values = None

            # resolve is_nullable, priority being True, then False, then None
            if a_column.is_nullable is None and b_column.is_nullable is None:
                is_nullable = None
            elif a_column.is_nullable or b_column.is_nullable:
                is_nullable = True
            else:
                is_nullable = False

            # resolve value range
            value_range_min = a_column.value_range_min
            if b_column.value_range_min is not None:
                if value_range_min is None:
                    value_range_min = b_column.value_range_min
                else:
                    value_range_min = min(value_range_min, b_column.value_range_min)
            value_range_max = a_column.value_range_max
            if b_column.value_range_max is not None:
                if value_range_max is None:
                    value_range_max = b_column.value_range_max
                else:
                    value_range_max = max(value_range_max, b_column.value_range_max)
            columns.append(
                Column(
                    a_column.name,
                    col_type,
                    possible_values,
                    is_nullable,
                    value_range_min,
                    value_range_max,
                )
            )

        # combine file lists
        files = info_a.files + info_b.files

        return cls(
            display_name, columns, files, data_type_version=CURRENT_DATA_TYPE_VERSION
        )

    @classmethod
    def as_combination(
        cls, infos: Iterable, display_name: str = 'combined_dataset'
    ) -> DatasetInfo:
        """Combines an iterable of compatible DatasetInfo objects into one
        DatasetInfo"""
        return functools.reduce(
            lambda a, b: cls._combine(a, b, display_name=display_name), infos
        )

    @staticmethod
    def get_summary_dataframe(dataset_info: DatasetInfo) -> pd.DataFrame:
        """Returns a table (pandas DataFrame) summarizing the DatasetInfo."""
        return _summary_dataframe_for_columns(dataset_info.columns)

    def __repr__(self) -> str:
        column_info = textwrap.indent(repr(self.get_summary_dataframe(self)), '    ')
        return (
            f'DatasetInfo:\n'
            f'  display_name: {self.display_name}\n'
            f'  files: {self.files}\n'
            f'  columns:\n'
            f'{column_info}'
        )

    def _repr_html_(self) -> str:
        column_info = self.get_summary_dataframe(self)
        return (
            f'<div style="border: thin solid rgb(41, 57, 141); padding: 10px;">'
            f'<h3 style="text-align: center; margin: auto;">DatasetInfo\n</h3>'
            f'<pre>display_name: {self.display_name}\nfiles: {self.files}\n</pre>'
            f'<hr>Columns:'
            f'{column_info._repr_html_()}'
            f'</div>'
        )

    def _col_id_from_name(self, name: str) -> int:
        """Look up the index of the column by name"""
        for i, c in enumerate(self.columns):
            if c.name == name:
                return i
        raise KeyError(name)

    def __getitem__(self, item: str) -> List:
        return self.columns[self._col_id_from_name(item)]

    def __setitem__(self, key: str, value: Column) -> None:
        assert isinstance(value, Column), (  # nosec
            'Must set column to be a ' '`Column` object'
        )
        self.columns[self._col_id_from_name(key)] = value

    def __delitem__(self, key: str) -> None:
        del self.columns[self._col_id_from_name(key)]

    def validate(self) -> None:
        sanitized_name_dict: Dict[str, Any] = dict()
        validate_sanitized_names(self.columns, sanitized_name_dict)


class ModelInfo:

    """Information about a model. Stored in `model.yaml` file on the backend.

    :param display_name: [Deprecated in 1.7.0 and will be removed from 2.0.0 version.]
    A name for user-facing display (different from an id).
    :param input_type: Specifies whether the model is in the tabular or text
        paradigm.
    :param model_task: Specifies the task the model is designed to address.
    :param inputs: A list of Column objects corresponding to the dataset
        columns that are fed as inputs into the model.
    :param outputs: A list of Column objects corresponding to the table
        output by the model when running predictions.
    :param targets: A list of Column objects corresponding to the dataset
        columns used as targets/labels for the model. If not provided, some
        functionality (like scoring) will not be available.
    :param algorithm: A string providing information about the model type.
    :param framework: A string providing information about the software library
        and version used to train and run this model.
    :param description: A user-facing description of the model.
    :param datasets: A list of dataset names assocated with this model.
    :param weighting_params: [Optional] Weighting parameters to account for class-imbalance. These parameters
        will be used to generate reference and production histograms.
    :param preferred_explanation_method: [Optional] Specifies a preference
        for the default explanation algorithm.  Front-end will choose
        explanation method if unspecified (typically Fiddler Shapley).
        Must be one of the built-in explanation types (ie an `fdl.core_objects.ExplanationMethod`) or be specified as
        a custom explanation type via `custom_explanation_names` (and in `package.py`).
    :param custom_explanation_names:
    [Optional] List of (string) names that
        can be passed to the explanation_name argument of the optional
        user-defined explain_custom method of the model object defined in
        package.py. The `preferred_explanation_method` can be set to one of these in order to override built-in explanations.
    :param binary_classification_threshold: [Optional] Float representing threshold for labels
    :param ranking_top_k: [Optional] Int used only for Ranking models and representing the top k results to take into
     consideration when computing performance metrics like MAP and NDCG.
    :param group_by: [Optional] A string representing the column name performance metrics have
     to be group by with for performance metrics computation. This have to be given for Ranking for MAP
      and NDCG computations. For ranking models, it represents the query/session id column.
    :param missing_value_encodings(fall_back): [Optional] A dictionary of list representing the values that should be
           replaced with null for each columns. Key is the column name.
    :param tree_shap_enabled: [Optional] Boolean value indicating if Tree SHAP should be enabled for this model.
           If set to True, Tree SHAP will become the default explanation method unless you specify another
           preferred explanation method.
    :param custom_features: [Optional] A list of custom features.
    :param data_type_version: [Optional] a String indicating 'v0', 'v1' etc. Used mainly to apply data type conversion rules.
    :param **kwargs: Additional information about the model to store as `misc`.
    """

    def __init__(
        self,
        display_name: str,
        input_type: ModelInputType,
        model_task: ModelTask,
        inputs: Optional[List[Column]] = None,
        outputs: Optional[List[Column]] = None,
        targets: Optional[List[Column]] = None,
        target_class_order: Optional[List] = None,
        metadata: Optional[List[Column]] = None,
        decisions: Optional[List[Column]] = None,
        algorithm: Optional[str] = None,
        framework: Optional[str] = None,
        description: Optional[str] = None,
        datasets: Optional[List[str]] = None,
        weighting_params: Optional[WeightingParams] = None,
        artifact_status: Optional[ArtifactStatus] = None,
        preferred_explanation_method: Optional[str] = None,
        custom_explanation_names: Optional[List[str]] = None,
        binary_classification_threshold: Optional[float] = None,
        ranking_top_k: Optional[int] = None,
        group_by: Optional[str] = None,
        fall_back: Optional[Dict] = None,
        missing_value_encodings: Optional[Dict] = None,
        tree_shap_enabled: Optional[bool] = False,
        custom_features: Optional[List[CustomFeature]] = None,
        is_binary_ranking_model: Optional[bool] = None,
        data_type_version: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        self.display_name = display_name
        self.input_type = input_type
        self.model_task = model_task
        self.inputs = inputs
        self.outputs = outputs
        self.targets = targets
        self.target_class_order = target_class_order
        self.metadata = metadata
        self.decisions = decisions
        self.algorithm = algorithm
        self.framework = framework
        self.description = description
        self.datasets = datasets
        self.weighting_params = weighting_params
        self.artifact_status = artifact_status
        self.binary_classification_threshold = binary_classification_threshold
        self.ranking_top_k = ranking_top_k
        self.schema_version = CURRENT_MODELINFO_SCHEMA_VERSION
        self.custom_features = custom_features
        self.data_type_version = data_type_version

        self.is_binary_ranking_model = is_binary_ranking_model

        self._validate_columns()

        self.target_class_order = self.get_target_class_order(
            self.target_class_order, self.model_task, self.targets
        )

        if model_task == ModelTask.RANKING:
            if group_by is None:
                raise ValueError(
                    'The argument group_by cannot be empty for Ranking models'
                )
            self.is_binary_ranking_model = len(self.target_class_order) == 2  # type: ignore

        self.group_by = group_by

        # artifact_status is set by Model Service
        # POST /v2/models sets  artifact_status to NO_MODEL
        # POST /v2/<model-id>/deploy-artifacts/... sets USER_UPLOADED
        # POST /v2/<model-id>/deploy-surrogate sets SURROGATE
        if artifact_status is not None:
            self.warn_deprecated_parameter(
                param_name='artifact_status', from_version='1.7'
            )

        if custom_explanation_names is None:
            custom_explanation_names = []

        if tree_shap_enabled:
            custom_explanation_names.append('Tree Shap')
            if preferred_explanation_method is None:
                preferred_explanation_method = 'Tree Shap'

        # we only store strings, not enums
        if isinstance(preferred_explanation_method, ExplanationMethod):
            preferred_explanation_method = preferred_explanation_method.value

        # Prevent the user from overloading a built-in.
        duplicated_names = []
        for name in custom_explanation_names:
            if type(name) != str:
                raise ValueError(
                    f'custom_explanation_names for ModelInfo must all be of '
                    f"type 'str', but '{name}' is of type '{type(name)}'"
                )
            if name in BUILT_IN_EXPLANATION_NAMES:
                duplicated_names.append(name)
        if len(duplicated_names) > 0:
            raise ValueError(
                f'Please select different names for your custom explanations. '
                f'The following are reserved built-ins duplicated in your custom '
                f'explanation names: {duplicated_names}.'
            )

        # Prevent the user from defaulting to an explanation that doesn't exist
        if (
            preferred_explanation_method is not None
            and preferred_explanation_method not in BUILT_IN_EXPLANATION_NAMES
            and preferred_explanation_method not in custom_explanation_names
        ):
            if len(custom_explanation_names) > 0:
                raise ValueError(
                    f'The preferred_explanation_method specified ({preferred_explanation_method}) could not be found '
                    f'in the built-in explanation methods ({BUILT_IN_EXPLANATION_NAMES}) or in the '
                    f'custom_explanation_names ({custom_explanation_names})'
                )
            else:
                raise ValueError(
                    f'The preferred_explanation_method specified ({preferred_explanation_method}) could not be found '
                    f'in the built-in explanation methods ({BUILT_IN_EXPLANATION_NAMES})'
                )

        self.preferred_explanation_method = preferred_explanation_method
        self.custom_explanation_names = custom_explanation_names
        self.misc = kwargs

        if fall_back is not None:
            LOG.warning(
                'WARNING: fall_back will be deprecated in a future version. '
                'Use missing_value_encodings instead. '
            )
        if missing_value_encodings is None:
            self.missing_value_encodings = fall_back
        else:
            self.missing_value_encodings = missing_value_encodings
            if fall_back is not None and fall_back != missing_value_encodings:
                LOG.warning(
                    'WARNING: Both missing_value_encodings and fall_back are specified,'
                    ' accept missing_value_encodings and ignore fall_back. '
                )
        if self.missing_value_encodings is not None:
            ModelInfo.validate_missing_value_encodings(
                self.missing_value_encodings, self.get_all_cols()
            )
        self.fall_back = self.missing_value_encodings  # backward compatability

        if self.custom_features is not None:
            if not isinstance(self.custom_features, List):
                raise ValueError(
                    'The custom_features argument only accepts a list of CustomFeature objects.'
                )

            available_cols = (
                self.get_input_names()
                + self.get_target_names()
                + self.get_metadata_names()
            )
            numeric_cols = self.get_input_pandas_dtypes()
            if self.metadata:
                numeric_cols.update(self.get_metadata_pandas_dtypes())
            if self.targets:
                numeric_cols.update(self.get_target_pandas_dtypes())
            valid_col_names = [
                k
                for k, v in numeric_cols.items()
                if v in (DataType.INTEGER.value, DataType.FLOAT.value)
            ]
            valid_vector_cols = [
                input.name for input in self.inputs if input.data_type.is_vector()
            ]

            unique_cf_names = []
            for feature in self.custom_features:
                if not isinstance(feature, CustomFeature):
                    raise ValueError(
                        'The custom_features argument only accepts a list of CustomFeature objects.'
                    )

                if feature.name in available_cols:
                    raise ValueError(
                        f'A column name "{feature.name}" already exists in the dataset. Please use a different name for custom feature {feature}.'
                    )

                if feature.name in unique_cf_names:
                    raise ValueError(
                        f'Multiple custom features are defined with the same name {feature.name}.'
                    )
                else:
                    unique_cf_names.append(feature.name)

                if isinstance(feature, (TextEmbedding, ImageEmbedding, VectorFeature)):
                    if not feature.column in valid_vector_cols:
                        raise ValueError(
                            f"Custom features '{feature.name}' defined on column '{feature.column}' is not found"
                        )
                else:
                    for col in feature.columns:  # type: ignore
                        if col not in valid_col_names:
                            raise ValueError(
                                f"Custom features '{feature.name}' defined on column '{col}' is not found or not of type int/float."
                            )

    def warn_deprecated_parameter(self, param_name: str, from_version: str) -> None:
        warnings.warn(
            f'WARNING: {param_name} is deprecated in {from_version}. It will be removed from 2.0.0 version.',
            DeprecationWarning,
        )

    def to_dict(self) -> Dict:
        """Dumps to basic python objects (easy for JSON serialization)"""
        res: Dict[str, Any] = {
            'name': self.display_name,
            'input-type': self.input_type.value,
            'model-task': self.model_task.value,
            'datasets': self.datasets or [],
        }
        if self.inputs:
            res['inputs'] = [col.to_dict() for col in self.inputs]
        if self.outputs:
            res['outputs'] = [col.to_dict() for col in self.outputs]
        if self.targets:
            res['targets'] = [col.to_dict() for col in self.targets]
        if self.target_class_order is not None:
            res['target-class-order'] = self.target_class_order
        if self.metadata:
            res['metadata'] = [metadata_col.to_dict() for metadata_col in self.metadata]
        if self.decisions:
            res['decisions'] = [
                decision_col.to_dict() for decision_col in self.decisions
            ]
        if self.description is not None:
            res['description'] = self.description
        if self.algorithm is not None:
            res['algorithm'] = self.algorithm
        if self.framework is not None:
            res['framework'] = self.framework
        if self.artifact_status is not None:
            res['artifact_status'] = self.artifact_status.value
        if self.preferred_explanation_method is not None:
            res['preferred-explanation-method'] = self.preferred_explanation_method
        if self.binary_classification_threshold is not None:
            res[
                'binary_classification_threshold'
            ] = self.binary_classification_threshold
        if self.ranking_top_k is not None:
            res['ranking_top_k'] = self.ranking_top_k
        if self.group_by is not None:
            res['group_by'] = self.group_by
        if self.schema_version is not None:
            res['schema_version'] = self.schema_version
        else:
            # Default schema version for old non-handled cases
            res['schema_version'] = DEFUNCT_MODELINFO_SCHEMA_VERSION
        if self.fall_back is not None:
            res['fall_back'] = self.fall_back
        if self.missing_value_encodings is not None:
            res['missing_value_encodings'] = self.missing_value_encodings
        res['custom-explanation-names'] = self.custom_explanation_names
        if self.custom_features is not None:
            res['custom_features'] = [f.to_dict() for f in self.custom_features]
        if self.weighting_params is not None:
            res['weighting_params'] = self.weighting_params.to_dict()
        if self.is_binary_ranking_model is not None:
            res['is_binary_ranking_model'] = self.is_binary_ranking_model
        if self.data_type_version is not None:
            res['data_type_version'] = self.data_type_version
        return {**res, **self.misc}

    @classmethod  # noqa: C901
    def from_dict(cls, deserialized_json: dict) -> ModelInfo:
        """Transforms deserialized JSON into a ModelInfo object"""
        # drop down into the "model" object inside the deserialized_json
        # (work on a copy)
        if 'model' in deserialized_json:
            deserialized_json = copy.deepcopy(deserialized_json['model'])
        else:
            deserialized_json = copy.deepcopy(deserialized_json)

        name = deserialized_json.pop('name')
        input_type = ModelInputType(deserialized_json.pop('input-type'))
        model_task = ModelTask(deserialized_json.pop('model-task'))

        inputs: Optional[List[Column]] = None
        if 'inputs' in deserialized_json:
            inputs = [Column.from_dict(c) for c in deserialized_json.pop('inputs')]

        outputs: Optional[List[Column]] = None
        if 'outputs' in deserialized_json:
            outputs = [Column.from_dict(c) for c in deserialized_json.pop('outputs')]

        if 'target-class-order' in deserialized_json:
            target_class_order = deserialized_json.pop('target-class-order')
        else:
            target_class_order = None

        artifact_status: Optional[ArtifactStatus] = None
        if 'artifact_status' in deserialized_json:
            artifact_status = ArtifactStatus(deserialized_json.pop('artifact_status'))

        metadata: Optional[List[Column]] = None
        if 'metadata' in deserialized_json:
            metadata = [Column.from_dict(c) for c in deserialized_json.pop('metadata')]

        decisions: Optional[List[Column]] = None
        if 'decisions' in deserialized_json:
            decisions = [
                Column.from_dict(c) for c in deserialized_json.pop('decisions')
            ]

        targets: Optional[List[Column]] = None
        if 'targets' in deserialized_json:
            targets = [Column.from_dict(c) for c in deserialized_json.pop('targets')]

        if 'missing_value_encodings' in deserialized_json:
            missing_value_encodings = deserialized_json.pop('missing_value_encodings')
        else:
            missing_value_encodings = None
        if 'fall_back' in deserialized_json:
            fall_back = deserialized_json.pop('fall_back')
        else:
            fall_back = None

        if 'tree_shap_enabled' in deserialized_json:
            tree_shap_enabled = deserialized_json.pop('tree_shap_enabled')
        else:
            tree_shap_enabled = False

        description = deserialized_json.pop('description', None)
        algorithm = deserialized_json.pop('algorithm', None)
        framework = deserialized_json.pop('framework', None)
        datasets: Optional[Any] = None
        if 'datasets' in deserialized_json:
            datasets = deserialized_json.pop('datasets')

        preferred_explanation_method: Optional[Any] = None
        if 'preferred-explanation-method' in deserialized_json:
            preferred_explanation_method = deserialized_json.pop(
                'preferred-explanation-method'
            )

        custom_explanation_names: List[Any] = []
        if 'custom-explanation-names' in deserialized_json:
            custom_explanation_names = deserialized_json.pop('custom-explanation-names')

        binary_classification_threshold: Optional[float] = None
        if model_task == ModelTask.BINARY_CLASSIFICATION:
            # @TODO: https://fiddlerlabs.atlassian.net/browse/FDL-4090
            try:
                binary_classification_threshold = float(
                    deserialized_json.pop('binary_classification_threshold')
                )
            except Exception:
                # Default to 0.5
                LOG.warning(
                    'No `binary_classification_threshold` specified, defaulting to 0.5'
                )
                binary_classification_threshold = 0.5

        ranking_top_k: Optional[int] = None
        group_by: Optional[str] = None
        is_binary_ranking_model: Optional[bool] = None
        if model_task == ModelTask.RANKING:
            try:
                ranking_top_k = int(deserialized_json.pop('ranking_top_k'))
            except Exception:
                # Default to 50
                LOG.warning('No `ranking_top_k` specified, defaulting to 50')
                ranking_top_k = 50
            group_by = deserialized_json.pop('group_by')
            if 'is_binary_ranking_model' in deserialized_json:
                is_binary_ranking_model = deserialized_json.pop(
                    'is_binary_ranking_model'
                )

        schema_version = deserialized_json.pop(
            'schema_version', DEFUNCT_MODELINFO_SCHEMA_VERSION
        )

        weighting_params: Optional[WeightingParams] = None
        if 'weighting_params' in deserialized_json:
            weighting_params = WeightingParams.from_dict(
                deserialized_json.pop('weighting_params')
            )
        custom_features: Optional[List[CustomFeature]] = None
        if 'custom_features' in deserialized_json:
            custom_features = [
                CustomFeature.from_dict(d)
                for d in deserialized_json.pop('custom_features')
            ]

        data_type_version: Optional[str] = None
        if 'data_type_version' in deserialized_json:
            data_type_version = deserialized_json.pop('data_type_version')

        # instantiate the class
        model_info = cls(
            display_name=name,
            input_type=input_type,
            model_task=model_task,
            inputs=inputs,
            outputs=outputs,
            target_class_order=target_class_order,
            metadata=metadata,
            decisions=decisions,
            targets=targets,  # type: ignore
            description=description,
            algorithm=algorithm,
            framework=framework,
            datasets=datasets,
            weighting_params=weighting_params,
            artifact_status=artifact_status,
            preferred_explanation_method=preferred_explanation_method,
            custom_explanation_names=custom_explanation_names,
            binary_classification_threshold=binary_classification_threshold,
            ranking_top_k=ranking_top_k,
            group_by=group_by,
            fall_back=fall_back,
            missing_value_encodings=missing_value_encodings,
            tree_shap_enabled=tree_shap_enabled,
            custom_features=custom_features,
            is_binary_ranking_model=is_binary_ranking_model,
            data_type_version=data_type_version,
            **deserialized_json,
        )
        # Explicitly set the version number
        model_info.schema_version = schema_version
        return model_info

    def _validate_columns(self) -> None:
        """
        validate if required columns are provided in constructor and populate target_class_order
        """
        if self.model_task in {ModelTask.NOT_SET, ModelTask.LLM}:
            return

        if not self.inputs:
            raise ValueError('Model inputs not specified')

        if not self.outputs:
            raise ValueError('Model outputs not specified')

        if not self.targets:
            raise ValueError('Model targets not specified')

        if not isinstance(self.targets, list) or len(self.targets) != 1:
            raise ValueError('Model target must be a list of Column with length 1')

    @staticmethod
    def validate_missing_value_encodings(
        missing_value_encodings: dict, all_columns: List[Column]
    ) -> None:
        unmatched_col = []
        if not isinstance(missing_value_encodings, dict):
            raise ValueError(
                f'Type dictionary expected for missing_value_encodings parameter. '
                f'Instead, found type {type(missing_value_encodings)}.'
            )
        for k, v in missing_value_encodings.items():
            matched_column = None
            for column in all_columns:
                if k == column.name:
                    matched_column = column
            if matched_column is None:
                LOG.warning(
                    f'WARNING: Missing_value_encodings(fall_back): Column {k} '
                    f'Not found in all column names. Dropping it.'
                )
                unmatched_col.append(k)
            else:
                # check if the column is specified as is_nullable
                if (
                    matched_column.is_nullable is not None
                    and matched_column.is_nullable is False
                ):
                    matched_column.is_nullable = True
                    LOG.warning(
                        f'Columns in Missing_value_encodings(fall_back) should be nullable. '
                        f'Change Column({k}) to nullable. '
                    )
                # prevent the user from specifying an invalid schema for missing_value_encodings
                if not isinstance(v, List):
                    raise ValueError(
                        f'Missing_value_encodings(fall_back) specified for Column({k}) has to be a list, '
                        f'instead got type of {type(v)}'
                    )
                for ind, value in enumerate(v):
                    if matched_column.data_type.value == DataType.FLOAT.value:
                        if value == float('inf'):
                            missing_value_encodings[k][ind] = 'inf'
                        elif value == -float('inf'):
                            missing_value_encodings[k][ind] = '-inf'

        for k in unmatched_col:
            del missing_value_encodings[k]
        if len(missing_value_encodings) == 0:
            raise ValueError(
                'None of the missing_value_encodings(fall_back) matches the column names entered, please provide '
                'dictionary with valid keys.'
            )

    @staticmethod
    def _infer_target_class_order(
        target_column: Column, model_task: ModelTask
    ) -> Union[List[int | float], List[bool]]:
        '''
        function is called when users don't provide target-class-order when creating
        model-info object, from __init__ and from_dataset_info.
        -regression: None
        -binary_classification:
            -numeric: infer from value-range-min & value-range-max
            -boolean: infer as [False, True]
            -category: should be manually provided
        -multiclass_classification: should be manually provided
        -ranking: should be manually provided
        '''
        if (
            target_column.data_type.is_numeric()
            and model_task == ModelTask.BINARY_CLASSIFICATION
        ):
            if (
                target_column.value_range_max is None
                or target_column.value_range_min is None
            ):
                raise ValueError(
                    f'Target {target_column.name} does not have 2 unique non null '
                    f'values.'
                )
            if target_column.value_range_max == target_column.value_range_min:
                raise ValueError(
                    f'Target {target_column.name} has only one unique value.'
                )

            return [target_column.value_range_min, target_column.value_range_max]
        if target_column.data_type == DataType.BOOLEAN:
            return [False, True]

        # For other cases, target_class_order has to be specified
        raise ValueError(
            f'Target-class-order(categorical_target_class_details) must be defined for '
            f'task type {model_task} when target is of type '
            f'{target_column.data_type}.'
        )

    def get_input_names(self) -> List[str]:
        """Returns a list of names for model inputs."""
        return [column.name for column in self.inputs or []]

    def get_output_names(self) -> List[str]:
        """Returns a list of names for model outputs."""
        return [column.name for column in self.outputs or []]

    def get_metadata_names(self) -> Union[List, List[str]]:
        """Returns a list of names for model metadata."""
        return [column.name for column in self.metadata or []]

    def get_decision_names(self) -> Union[List, List[str]]:
        """Returns a list of names for model decisions."""
        return [column.name for column in self.decisions or []]

    def get_target_names(self) -> List[str]:
        """Returns a list of names for model targets."""
        return [column.name for column in self.targets or []]

    def get_input_pandas_dtypes(
        self,
    ) -> Dict[str, Union[str, CategoricalDtype]]:
        """Get a dictionary describing the pandas datatype of every input."""
        return _get_field_pandas_dtypes(self.inputs)

    def get_output_pandas_dtypes(
        self,
    ) -> Dict[str, Union[str, CategoricalDtype]]:
        """Get a dictionary describing the pandas datatype of every output."""
        return _get_field_pandas_dtypes(self.outputs)

    def get_metadata_pandas_dtypes(
        self,
    ) -> Dict[str, Union[str, CategoricalDtype]]:
        """Get a dictionary describing the pandas datatype of every
        metadata column."""
        assert self.metadata is not None
        return _get_field_pandas_dtypes(self.metadata)

    def get_decisions_pandas_dtypes(
        self,
    ) -> Dict[str, Union[str, CategoricalDtype]]:
        """Get a dictionary describing the pandas datatype of every decision
        column."""
        assert self.decisions is not None
        return _get_field_pandas_dtypes(self.decisions)

    def get_target_pandas_dtypes(
        self,
    ) -> Dict[str, Union[str, CategoricalDtype]]:
        """Get a dictionary describing the pandas datatype of every target."""
        assert self.targets is not None
        return _get_field_pandas_dtypes(self.targets)

    def get_non_monitor_components(self) -> Set:
        """
        return a set of column names which are part of custom_features but are not
        monitored as individual features.
        If a column is found in multiple custom_features with different monitor_components
        value, True overwrites False and it is not a part of non-monitor-components
        return an empty set if no custom_features
        """
        non_monitor: Set = set()
        if not self.custom_features:
            return non_monitor
        monitor: Set = set()
        for cf in self.custom_features:
            if getattr(cf, 'monitor_components', False):
                monitor.update(cf.columns)  # type: ignore
            else:
                non_monitor.update(cf.columns)  # type: ignore
        non_monitor = non_monitor - monitor
        return non_monitor

    @classmethod  # noqa: C901
    def from_dataset_info(
        cls,
        dataset_info: DatasetInfo,
        target: Optional[List[str]] = None,
        dataset_id: Optional[str] = None,
        features: Optional[List[str]] = None,
        fall_back: Optional[Dict] = None,
        missing_value_encodings: Optional[Dict] = None,
        metadata_cols: Optional[List[str]] = None,
        decision_cols: Optional[List[str]] = None,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        algorithm: Optional[str] = None,
        framework: Optional[str] = None,
        input_type: ModelInputType = ModelInputType.TABULAR,
        model_task: Optional[ModelTask] = None,
        outputs: Optional[Any] = None,
        categorical_target_class_details: Optional[Any] = None,
        weighting_params: Optional[WeightingParams] = None,
        preferred_explanation_method: Optional[str] = None,
        custom_explanation_names: Optional[List[str]] = None,
        binary_classification_threshold: Optional[float] = None,
        ranking_top_k: Optional[int] = None,
        group_by: Optional[str] = None,
        tree_shap_enabled: Optional[bool] = False,
        custom_features: Optional[List[CustomFeature]] = None,
    ) -> ModelInfo:
        """Produces a ModelInfo for a model trained on a dataset.

        :param dataset_info: A DatasetInfo object describing the training
            dataset.
        :param target: The list of column names of the target(s) the model predicts.
        :param dataset_id: Specify the dataset_id for the model. Must be provided if the dataset_id cannot be inferred from the dataset_info.
        :param features: A list of column names for columns used as features.
        :param missing_value_encodings(fall_back): A dictionary of list representing the values that should be
           replaced with null for each columns. Key is the column name.
        :param metadata_cols: A list of column names for columns used as
        metadata.
        :param decision_cols: A list of column names for columns used as
        decisions.
        :param display_name: A model name for user-facing display (different
            from an id).
        :param description: A user-facing description of the model.
        :param algorithm: A string providing information about the model type.
        :param framework: A string providing information about the software library
            and version used to train and run this model.
        :param input_type: Specifies the paradigm (tabular or text) of the
            model.
        :param model_task: Specifies the prediction task addressed by the
            model. If not explicitly provided, this will be inferred from the
            data type of the target variable.
        :param outputs: model output names, if multiclass classification, must be a sequence in the same order as categorical_target_class_details.
            If binary classification, must be a single name signifying the probability of the positive class. # TODO: bulletproofing
            If regression/ranking, must be a dictionary of the form {column_name: (min_value, max_value)}, or a
            dictionary with empty range {column_name:[]} if column_name can be found in the dataset
        :param categorical_target_class_details: specify the output categories of your model (only applicable for classification and ranking models)
            This parameter *must* be provided for multiclass, binary-classification and ranking models where
            the target is of type CATEGORY. It is optional for binary classification with BOOLEAN targets, and ignored for regression.

            For multiclass classification models, provide a list of all the possible
            output categories of your model. The same order will be implicitly assumed
            by register model surrogate, and must match the outputs from custom package.py
            uploads. # TODO: ensure surrogate order matches this order.

            For binary classification models, if you provide a single element (or a list with
            a single element) then that element will be considered to be the positive class.
            Alternatively you can provide a list with 2 elements. The 0th element,
            by convention will be considered to be the negative class, and the 1th element will
            define the positive class. These params can be used to override the default convention
            specified below.

            For binary classification with target of type BOOLEAN:
                - by default `True` is the positive class for `True`/`False` targets.
                - by default `1` or `1.0` for `1`/`0` integer targets or `1.`/`0.` float targets,
            For other binary classification tasks on numeric types:
                - by default the higher of the two possible values will be considered the positive class.
            In all other cases, one of the two classes will arbitrarily be FIXED as the positive class.

            For ranking models, provide a list of all the possible target values in order of relevance. The first element will be considered
            as not relevant, the last element from the list will be considered the most relevant grade.
        :param weighting_params: [Optional] Weighting parameters to account for class-imbalance. These parameters
            will be used to generate reference and production histograms.
        :param preferred_explanation_method: [Optional] Specifies a preference
            for the default explanation algorithm.  Front-end will choose
            explanaton method if unspecified (typically Fiddler Shapley).
            Providing ExplanationMethod.CUSTOM will cause the first of the
            custom_explanation_names to be the default (which must be defined
            in that case).
        :param custom_explanation_names: [Optional] List of names that
            can be passed to the explanation_name argument of the optional
            user-defined explain_custom method of the model object defined in
            package.py.
        :param binary_classification_threshold: [Optional] Float representing threshold for labels
        :param ranking_top_k: [Optional] Int used only for Ranking models and representing the top k results to take into
         consideration when computing performance metrics like MAP and NDCG.
        :param group_by: [Optional] A string representing the column name performance metrics have
         to be group by with for performance metrics computation. This have to be given for Ranking for MAP
          and NDCG computations. For ranking models, it represents the query/session id column.
        :param tree_shap_enabled: [Optional] Boolean value indicating if Tree SHAP should be enabled for this model.
           If set to True, Tree SHAP will become the default explanation method unless you specify another
           preferred explanation method.
        :param custom_features: [Optional] A list of custom features that are instances of CustomFeature class.

        :returns A ModelInfo object.
        """
        if categorical_target_class_details is not None:
            warnings.warn(
                'WARNING: categorical_target_class_details is deprecated in 1.7 and '
                'will be removed from 2.0.0 version. categorical_target_class_details '
                'will be replaced by target_class_order in 2.0.0',
                DeprecationWarning,
            )

        if custom_explanation_names is None:
            custom_explanation_names = []

        if not isinstance(dataset_info, DatasetInfo):
            raise ValueError(
                f'The dataset_info parameter must be a valid DatasetInfo object'
            )

        if display_name is None:
            if dataset_info.display_name is not None:
                display_name = f'{dataset_info.display_name} model'
            else:
                display_name = ''

        additional_cols = cls.get_additional_cols(
            metadata_cols=metadata_cols,
            decision_cols=decision_cols,
            outputs=outputs,
            targets=target,
            features=features,
        )

        # todo (pradhuman): replace categorical_target_class_details with target_class_order

        if not model_task:
            raise ValueError(
                'model_task is required to create a model info. Please specify a value '
                'using the ModelTask enum.'
            )

        target_columns = cls.get_target_columns(
            targets=target, dataset_info=dataset_info, model_task=model_task
        )

        (
            is_binary_ranking_model,
            ranking_top_k,
            binary_classification_threshold,
        ) = cls.get_model_parameters(
            model_task=model_task,
            target_columns=target_columns,
            ranking_top_k=ranking_top_k,
            binary_classification_threshold=binary_classification_threshold,
        )

        if isinstance(outputs, str):
            outputs = [outputs]

        if isinstance(outputs, dict):
            output_names = list(outputs.keys())
        else:
            output_names = outputs  # type: ignore
        cls.validate_model_task(
            model_task=model_task,
            target_columns=target_columns,
            output_names=output_names,
        )

        target_class_order = None
        if target_columns:
            target_class_order = cls.get_target_class_order(
                model_task=model_task,
                target_columns=target_columns,
                target_class_order=categorical_target_class_details,
            )

        if not outputs:
            outputs = cls.infer_output_names(
                model_task=model_task,
                target_columns=target_columns,
                target_class_order=target_class_order,
            )

        output_columns = cls.get_outputs(
            output_names=outputs,
            target_columns=target_columns,
            dataset_info=dataset_info,
            model_task=model_task,
        )

        inputs, metadata, decisions = cls.get_inputs_metadata_decisions(
            dataset_info=dataset_info,
            features=features,
            metadata_cols=metadata_cols,
            decision_cols=decision_cols,
            additional_cols=additional_cols,
            targets=target,
            outputs=outputs,
        )

        if (model_task not in {ModelTask.LLM, ModelTask.NOT_SET}) and (not inputs):
            raise ValueError(
                'None of the features specified were found in the DatasetInfo object. '
                'Ensure that the features specified are present in the dataset you '
                'are using.'
            )

        cls.check_input_type(input_type=input_type, inputs=inputs)

        cls.check_weighting_params(
            weighting_params=weighting_params,
            model_task=model_task,
            target_class_order=target_class_order,
        )

        return cls(
            display_name=display_name,
            description=description,
            algorithm=algorithm,
            framework=framework,
            input_type=input_type,
            model_task=model_task,
            datasets=None,
            inputs=inputs,
            outputs=output_columns,  # type: ignore
            target_class_order=target_class_order,
            metadata=metadata,
            decisions=decisions,
            targets=target_columns,
            weighting_params=weighting_params,
            preferred_explanation_method=preferred_explanation_method,
            custom_explanation_names=custom_explanation_names,
            binary_classification_threshold=binary_classification_threshold,
            ranking_top_k=ranking_top_k,
            group_by=group_by,
            fall_back=fall_back,
            missing_value_encodings=missing_value_encodings,
            tree_shap_enabled=tree_shap_enabled,
            custom_features=custom_features,
            is_binary_ranking_model=is_binary_ranking_model,
            data_type_version=dataset_info.data_type_version,
        )

    @staticmethod
    def get_summary_dataframes_dict(model_info: ModelInfo) -> Dict[str, pd.DataFrame]:
        """Returns a dictionary of DataFrames summarizing the
        ModelInfo's inputs, outputs, and if they exist, metadata
        and decisions"""

        summary_dict = dict()

        if model_info.inputs:
            summary_dict['inputs'] = _summary_dataframe_for_columns(model_info.inputs)

        if model_info.outputs:
            summary_dict['outputs'] = _summary_dataframe_for_columns(model_info.outputs)

        if model_info.metadata:
            summary_dict['metadata'] = _summary_dataframe_for_columns(
                model_info.metadata
            )
        if model_info.decisions:
            summary_dict['decisions'] = _summary_dataframe_for_columns(
                model_info.decisions
            )
        if model_info.targets:
            summary_dict['targets'] = _summary_dataframe_for_columns(model_info.targets)

        if model_info.custom_features:
            summary_dict['custom_features'] = _summary_dataframe_for_custom_features(
                model_info.custom_features
            )

        return summary_dict

    @classmethod
    def get_target_columns(
        cls,
        targets: Optional[List[str]],
        dataset_info: DatasetInfo,
        model_task: ModelTask,
    ) -> List[Column] | None:
        if not targets:
            if model_task in {ModelTask.LLM, ModelTask.NOT_SET}:
                return
            raise ValueError(
                f'target has to be provided for model task {model_task}. Please specify the target.'
            )

        if isinstance(targets, str):
            targets = [targets]

        if not isinstance(targets, list):
            raise ValueError(
                f'target should be of type list. You provided type: {type(targets)}.'
            )

        if (len(targets) != 1) and (
            model_task not in {ModelTask.LLM, ModelTask.NOT_SET}
        ):
            raise ValueError(
                f'For model task {model_task}, a single target has to be specified.'
            )

        # Get target columns
        target_columns = []
        for target in targets:
            if target in dataset_info.get_column_names():
                column = dataset_info[target]
                if column.data_type.value == DataType.STRING:  # type: ignore
                    raise ValueError(
                        f'Target column {column.name} cannot be of type '  # type: ignore
                        f'{column.data_type}.'  # type: ignore
                    )
                target_columns.append(column)
            else:
                raise ValueError(f'Target "{target}" not found in dataset.')

        return target_columns  # type: ignore

    @classmethod
    def get_additional_cols(
        cls,
        metadata_cols: Optional[List[str]],
        decision_cols: Optional[List[str]],
        outputs: Optional[Union[List[str], Dict[str, Union[int, float]]]],
        targets: Optional[List[str]],
        features: Optional[List[str]],
    ) -> List[str]:
        additional_cols: List[str] = []
        if metadata_cols is not None:
            additional_cols += list(metadata_cols)

        if decision_cols is not None:
            additional_cols += list(decision_cols)

        if isinstance(outputs, List):
            additional_cols += outputs
        elif isinstance(outputs, Dict):
            additional_cols += outputs.keys()

        # ensure that columns are not duplicated
        if len(additional_cols) > 0:
            col_list: List = []
            if targets is not None:
                col_list += targets
            if features is not None:
                col_list += features

            duplicated_cols = [col for col in additional_cols if col in col_list]

            if len(duplicated_cols) > 0:
                raise ValueError(
                    f'Cols can be either feature, target, outputs, metadata or '
                    f'decisions. Cols {",".join(duplicated_cols)} are present '
                    f'in more than one category.'
                )
        return additional_cols

    @classmethod
    def infer_output_names(
        cls,
        model_task: ModelTask,
        target_columns: Optional[List[Column]],
        target_class_order: Optional[List],
    ) -> List[str] | None:
        if model_task in {ModelTask.LLM, ModelTask.NOT_SET}:
            return
        if model_task.value == ModelTask.BINARY_CLASSIFICATION.value:
            return [f'probability_{target_columns[0].name}_{target_class_order[1]}']  # type: ignore
        if model_task.value == ModelTask.MULTICLASS_CLASSIFICATION.value:
            return [
                f'probability_{target_columns[0].name}_{class_name}'
                for class_name in target_class_order  # type: ignore
            ]
        # For regression and ranking
        return [f'predicted_{target_columns[0].name}']

    @classmethod
    def check_input_type(cls, input_type: ModelInputType, inputs: List[Column]) -> None:
        if input_type == ModelInputType.TEXT:
            if len(inputs) != 1:
                raise ValueError(
                    f'Text models may only contain a single feature column containing '
                    f'text data. Please remove any other non-text features from the '
                    f'features argument if you wish to add a text model. You can add '
                    f'other columns as metadata columns. If your model has multiple '
                    f'inputs please specify the input_type to {ModelInputType.TABULAR}.'
                )
            if inputs[0].data_type != DataType.STRING:
                raise ValueError(
                    'Text features must be of type STRING. Please double check the '
                    'data type of the feature column passed into the '
                    'features argument.'
                )

    @classmethod
    def check_weighting_params(
        cls,
        weighting_params: Optional[WeightingParams],
        model_task: ModelTask,
        target_class_order: Optional[List],
    ) -> None:
        # perform checks for weighting parameters
        if weighting_params is not None:
            if (
                weighting_params.class_weight is not None
                and model_task.value == ModelTask.BINARY_CLASSIFICATION.value
            ):
                if len(weighting_params.class_weight) != 2:
                    raise ValueError(
                        f'Expected a class weighting vector of length 2 for '
                        f'{model_task.value} task, instead received vector of length '
                        f'{len(weighting_params.class_weight)}.'
                    )
            elif (
                weighting_params.class_weight is not None
                and model_task == ModelTask.MULTICLASS_CLASSIFICATION
            ):
                if len(weighting_params.class_weight) != len(target_class_order):  # type: ignore
                    raise ValueError(
                        f'Expected a class weighting vector of length '  # type: ignore
                        f'{len(target_class_order)} for {model_task.value} task, '
                        f'instead received vector of length '
                        f'{len(weighting_params.class_weight)}.'
                    )
            elif not model_task.is_classification():
                LOG.warning(
                    'WARNING: Weighting parameter not supported for non-classification '
                    'tasks and will be ignored.'
                )

    @classmethod
    def check_binary_target(cls, target_column: Column) -> bool:
        if target_column.data_type.value in [
            DataType.INTEGER.value,
            DataType.FLOAT.value,
        ]:
            return (
                int(target_column.value_range_max) == 1  # type: ignore
                and int(target_column.value_range_min) in [0, -1]  # type: ignore
            ) or (
                target_column.data_type.value == DataType.INTEGER.value
                and target_column.value_range_max - target_column.value_range_min == 1  # type: ignore
            )
        else:
            return len(target_column.possible_values) == 2  # type: ignore

    @classmethod
    def get_inputs_metadata_decisions(
        cls,
        dataset_info: DatasetInfo,
        features: Optional[List[str]],
        metadata_cols: Optional[List[str]],
        decision_cols: Optional[List[str]],
        additional_cols: List[str],
        targets: Optional[List[str]],
        outputs: Optional[Union[List[str], Dict[str, Union[int, float]]]],
    ) -> Tuple[List[Column], Optional[List[Column]], Optional[List[Column]]]:
        inputs: List[Column] = []
        metadata: Optional[List[Column]] = None
        decisions: Optional[List[Column]] = None

        if metadata_cols:
            metadata = []
        if decision_cols:
            decisions = []

        for column in dataset_info.columns:
            col_name = column.name
            if (
                (not targets or col_name not in targets)
                and (not outputs or col_name not in outputs)
                and (not features or col_name in features)
                and (col_name not in additional_cols)
            ):
                inputs.append(column.copy())
            if metadata_cols and col_name in metadata_cols:
                assert metadata is not None, 'metadata unexpectedly None'
                metadata.append(column.copy())
            if decision_cols and col_name in decision_cols:
                assert decisions is not None, 'decisions unexpectedly None'
                decisions.append(column.copy())

        return inputs, metadata, decisions

    @classmethod
    def get_outputs(
        cls,
        output_names: Optional[Union[List[str], Dict[str, tuple]]],
        target_columns: Optional[List[Column]],
        dataset_info: DatasetInfo,
        model_task: ModelTask,
    ) -> Optional[List[Column]]:
        if not output_names:
            return

        output_columns = []
        ds_info_names_columns = {}
        for ds_column in dataset_info.columns:
            ds_info_names_columns[ds_column.name] = ds_column

        if model_task.is_classification():
            if isinstance(output_names, dict):
                output_names = list(output_names.keys())
            for name in output_names:
                if name in ds_info_names_columns:
                    output_columns.append(ds_info_names_columns[name])
                else:
                    output_columns.append(
                        Column(
                            name=name,
                            data_type=DataType.FLOAT,
                            is_nullable=False,
                            value_range_min=0.0,
                            value_range_max=1.0,
                        )
                    )
            return output_columns

        if isinstance(output_names, dict):
            for name in output_names.keys():
                values = output_names[name]
                if not isinstance(values, (list, tuple)) or len(values) != 2:
                    raise ValueError(
                        f'If outputs is a dictionary, the values should '
                        f'be a tuple of 2 values. Currently passing: '
                        f'{values} for output {name}. Please correct.'
                    )
                if name in ds_info_names_columns:
                    column = ds_info_names_columns[name]
                    if not (
                        column.data_type == DataType.FLOAT
                        or column.data_type == DataType.INTEGER
                    ):
                        raise ValueError(
                            f'Column {name} with type {column.data_type} can not be specified as output.'
                            f'Output column type has to be either INTEGER or FLOAT.'
                            f'Please correct.'
                        )
                    column.value_range_min = min(values)
                    column.value_range_max = max(values)
                    output_columns.append(column)
                else:
                    output_columns.append(
                        Column(
                            name=name,
                            data_type=DataType.FLOAT,
                            is_nullable=False,
                            value_range_min=float(min(values)),
                            value_range_max=float(max(values)),
                        )
                    )
            return output_columns

        if isinstance(output_names, list):
            for name in output_names:
                col = name
                if name not in dataset_info.get_column_names():
                    raise ValueError(
                        f'Output {name} is not present in the dataset. '
                        f'Please provide a dictionary with the range: '
                        f'{name}: (min_value, max_value).'
                    )
                output_columns.append(dataset_info[col])
            return output_columns
        return

    @classmethod
    def get_model_parameters(
        cls,
        model_task: ModelTask,
        target_columns: Optional[List[Column]],
        ranking_top_k: Optional[int],
        binary_classification_threshold: Optional[float],
    ) -> Tuple[Optional[bool], Optional[int], Optional[float]]:
        is_binary_ranking_model = None
        top_k = None
        bin_class_threshold = None

        if model_task.value == ModelTask.RANKING.value:
            if ranking_top_k and not isinstance(ranking_top_k, int):
                raise ValueError(
                    f'ranking_top_k should be of type int. '
                    f'Type {type(ranking_top_k)} was given.'
                )

            top_k = 50 if not ranking_top_k else ranking_top_k
            if target_columns:
                is_binary_ranking_model = False
                if ModelInfo.check_binary_target(target_column=target_columns[0]):
                    is_binary_ranking_model = True

        if model_task.value == ModelTask.BINARY_CLASSIFICATION.value:
            if binary_classification_threshold and not isinstance(
                binary_classification_threshold, (int, float)
            ):
                raise ValueError(
                    f'binary_classification_threshold should be a float. '
                    f'Type {type(binary_classification_threshold)} was given.'
                )

            bin_class_threshold = (
                0.5
                if not binary_classification_threshold
                else float(binary_classification_threshold)
            )
            LOG.warning(
                f'Using ' f'binary_classification_threshold={bin_class_threshold}'
            )
        return is_binary_ranking_model, top_k, bin_class_threshold

    @classmethod
    def validate_model_task(
        cls,
        model_task: ModelTask,
        target_columns: Optional[List[Column]],
        output_names: Optional[List[str]],
    ) -> None:
        if model_task.value == ModelTask.BINARY_CLASSIFICATION.value:
            if output_names and (len(output_names) > 1):
                raise ValueError(
                    f'Model task specified as {model_task} but you specified '
                    f'{len(output_names)} output columns. Please specify a single column: '
                    f'only the positive probability column is expected.'
                )
            if target_columns and not ModelInfo.check_binary_target(
                target_column=target_columns[0]
            ):
                raise ValueError(
                    f'The specified target column ({target_columns[0].name}) is not '
                    f'specified correctly for binary classification. Target should '
                    f'have 2 unique values if not numerical. For numerical target,'
                    f' should have range (-1, 1) or (0, 1). '
                    f'You passed: {target_columns[0]}. Please correct your target or '
                    f'change your model task.'
                )

        elif model_task.value == ModelTask.MULTICLASS_CLASSIFICATION.value:
            if output_names and len(output_names) < 3:
                raise ValueError(
                    f'Model task specified as {model_task} but you specified '
                    f'{len(output_names)} output columns. Please specify more '
                    f'than 2 columns.'
                )
            if (
                target_columns
                and output_names
                and (not target_columns[0].data_type.is_numeric())
                and (len(target_columns[0].possible_values) != len(output_names))  # type: ignore
            ):
                raise ValueError(
                    f'The specified target column ({target_columns[0].name}) has '  # type: ignore
                    f'{len(target_columns[0].possible_values)} unique values, but '
                    f'{len(output_names)} output columns were specified. For multiclass '
                    f'classification model, number classes should match the number '
                    f'of outputs.'
                )

        elif model_task.value == ModelTask.REGRESSION.value:
            if output_names and len(output_names) > 1:
                raise ValueError(
                    f'Model task specified as {model_task} but you specified '
                    f'{len(output_names)} output columns. Please specify a single column.'
                )
            if target_columns and not target_columns[0].data_type.is_numeric():
                raise ValueError(
                    f'Model task {model_task} cannot have a target of type '
                    f'{target_columns[0].data_type}. Only numerical targets are allowed.'
                )

        elif model_task.value == ModelTask.RANKING.value:
            if output_names and len(output_names) > 1:
                raise ValueError(
                    f'Model task specified as {model_task} but you specified '
                    f'{len(output_names)} output columns. Please specify a single column.'
                )

    @classmethod
    def get_target_class_order(
        cls,
        target_class_order: Optional[
            Union[List[Union[str, bool, float, int]], Union[str, bool, float, int]]
        ],
        model_task: ModelTask,
        target_columns: Optional[List[Column]],
    ) -> Union[None, List[int | float], List[bool], List]:
        if (
            model_task.value
            in {
                ModelTask.REGRESSION.value,
                ModelTask.NOT_SET.value,
                ModelTask.LLM.value,
            }
        ) or (not target_columns):
            return None

        target_column = target_columns[0]

        if isinstance(target_class_order, (str, int, float, bool)):
            target_class_order = [target_class_order]

        if isinstance(target_class_order, np.ndarray):
            target_class_order = target_class_order.tolist()

        if target_class_order and not isinstance(target_class_order, list):
            raise ValueError(
                'Target-class-order(categorical_target_class_details) cannot be of type '
                f'{type(target_class_order)}'
            )

        if not target_class_order:
            return cls._infer_target_class_order(target_column, model_task)

        for value in target_class_order:
            if not isinstance(value, (str, int, float, bool)):
                raise ValueError(
                    'Value in Target-class-order(categorical_target_class_details) '
                    f'cannot be of type {type(value)}. Please input strings, floats, '
                    f'integers, or booleans. '
                )
        if target_column.possible_values:
            for value in target_column.possible_values:
                if not isinstance(value, (str, int, float, bool)):
                    raise ValueError(
                        f'Value in target_column({target_column.name}).possible-values '
                        f'cannot be of type {type(value)}. Please input strings, '
                        'floats, integers, or booleans. '
                    )

        if model_task.value in [
            ModelTask.MULTICLASS_CLASSIFICATION.value,
            ModelTask.RANKING.value,
        ]:
            if not target_column.data_type.is_numeric() and set(
                target_column.possible_values  # type: ignore
            ) != set(target_class_order):
                raise ValueError(
                    'Target-class-order(categorical_target_class_details) '
                    f'{target_class_order} does not have the same elements as target '
                    f'column {target_column.name} : ({target_column.possible_values}).'
                )
            return target_class_order

        if model_task.value == ModelTask.BINARY_CLASSIFICATION.value:
            if (
                not target_column.data_type.is_numeric()
                and len(target_column.possible_values) != 2  # type: ignore
            ):
                raise ValueError(
                    'Target column must contain no more than two unique values when '  # type: ignore
                    f'model task is set to {model_task.value}. Instead, found '
                    f'{len(target_column.possible_values)} unique values.'
                )

            if len(target_class_order) > 2:
                raise ValueError(
                    'Target-class-order(categorical_target_class_details) cannot have '
                    f'more than 2 elements for model task {model_task}.'
                )

            if len(target_class_order) == 2:
                if target_column.data_type.is_bool_or_cat() and set(
                    target_column.possible_values  # type: ignore
                ) != set(target_class_order):
                    raise ValueError(
                        'Target-class-order(categorical_target_class_details) does not '
                        f'have the same elements as target column {target_column.name}'
                    )
                return target_class_order

            # We are in the case that target_class_order has a single element and this
            # element is the positive class. Reorder [negative class, positive class]
            positive_class = target_class_order[0]
            target_class_order = target_column.possible_values
            target_class_order.remove(positive_class)  # type: ignore
            target_class_order.append(positive_class)  # type: ignore

            return target_class_order

        return None

    def _repr_html_(self) -> str:
        summary_dict = ModelInfo.get_summary_dataframes_dict(self)
        class_order = (
            f'  target_class_order: {self.target_class_order}\n'
            if self.target_class_order is not None
            else ''
        )

        algorithm_info = (
            f'  framework: {self.algorithm}\n' if self.algorithm is not None else ''
        )
        framework_info = (
            f'  framework: {self.framework}\n' if self.framework is not None else ''
        )

        misc_info = json.dumps(self.misc, indent=2)
        target_info = (
            f"<hr>targets:{summary_dict['targets']._repr_html_()}"
            if self.targets is not None
            else ''
        )
        decisions_info = (
            f"<hr>decisions:{summary_dict['decisions']._repr_html_()}"
            if self.decisions is not None
            else ''
        )
        metadata_info = (
            f"<hr>metadata:{summary_dict['metadata']._repr_html_()}"
            if self.metadata is not None
            else ''
        )

        fall_back_info = (
            f'  fall_back: {self.fall_back}\n' if self.fall_back is not None else ''
        )
        missing_value_encodings_info = (
            f'  missing_value_encodings: {self.missing_value_encodings}\n'
            if self.missing_value_encodings is not None
            else ''
        )
        input_info = (
            f'<hr>inputs:{summary_dict["inputs"]._repr_html_()}'
            if self.inputs is not None
            else ''
        )
        output_info = (
            f'<hr>outputs:{summary_dict["outputs"]._repr_html_()}'
            if self.outputs is not None
            else ''
        )
        custom_features = (
            f'<hr>custom features:{summary_dict["custom_features"]._repr_html_()}'
            if self.custom_features is not None
            else ''
        )
        return (
            f'<div style="border: thin solid rgb(41, 57, 141); padding: 10px;">'
            f'<h3 style="text-align: center; margin: auto;">ModelInfo\n</h3><pre>'
            f'  display_name: {self.display_name}\n'
            f'  description: {self.description}\n'
            f'  input_type: {self.input_type}\n'
            f'  model_task: {self.model_task}\n'
            f'{class_order}'
            f'  preferred_explanation: {self.preferred_explanation_method}\n'
            f'  custom_explanation_names: {self.custom_explanation_names}\n'
            f'{algorithm_info}'
            f'{framework_info}'
            f'{fall_back_info}'
            f'{missing_value_encodings_info}'
            f'  misc: {misc_info}</pre>'
            f'{target_info}'
            f'{input_info}'
            f'{output_info}'
            f'{custom_features}'
            f'{decisions_info}'
            f'{metadata_info}'
            f'</div>'
        )

    def __repr__(self) -> str:
        summary_dict = ModelInfo.get_summary_dataframes_dict(self)
        input_info = (
            f'  inputs:\n' f"{textwrap.indent(repr(summary_dict['inputs']), '    ')}"
            if self.inputs is not None
            else ''
        )
        output_info = (
            f'  outputs:\n' f"{textwrap.indent(repr(summary_dict['outputs']), '    ')}"
            if self.outputs is not None
            else ''
        )
        custom_features_info = (
            f'  custom features:\n'
            f"{textwrap.indent(repr(summary_dict['custom_features']), '    ')}"
            if self.custom_features is not None
            else ''
        )
        class_order = (
            f'  target_class_order: {self.target_class_order}\n'
            if self.target_class_order is not None
            else ''
        )

        metadata_info = (
            f'  metadata:\n'
            f"{textwrap.indent(repr(summary_dict['metadata']), '    ')}"
            if self.metadata is not None
            else ''
        )

        decisions_info = (
            f'  decisions:\n'
            f"{textwrap.indent(repr(summary_dict['decisions']), '    ')}"
            if self.decisions is not None
            else ''
        )

        target_info = (
            f'  targets:\n' f"{textwrap.indent(repr(summary_dict['targets']), '    ')}"
            if self.targets is not None
            else ''
        )
        # target_info = f'  targets: {self.targets}\n' if self.targets is not None else ''
        algorithm_info = (
            f'  algorithm: {self.algorithm}\n' if self.algorithm is not None else ''
        )
        framework_info = (
            f'  framework: {self.framework}\n' if self.framework is not None else ''
        )

        fall_back_info = (
            f'  fall_back: {self.fall_back}\n' if self.fall_back is not None else ''
        )
        missing_value_encodings_info = (
            f'  missing_value_encodings: {self.missing_value_encodings}\n'
            if self.missing_value_encodings is not None
            else ''
        )
        data_type_version_info = (
            f'  data_type_version: {self.data_type_version}\n'
            if self.data_type_version is not None
            else ''
        )
        misc_info = textwrap.indent(json.dumps(self.misc, indent=2), '    ')
        return (
            f'ModelInfo:\n'
            f'  display_name: {self.display_name}\n'
            f'  description: {self.description}\n'
            f'  input_type: {self.input_type}\n'
            f'  model_task: {self.model_task}\n'
            f'{class_order}'
            f'  preferred_explanation: {self.preferred_explanation_method}\n'
            f'  custom_explanation_names: {self.custom_explanation_names}\n'
            f'{input_info}\n'
            f'{output_info}\n'
            f'{custom_features_info}\n'
            f'{metadata_info}\n'
            f'{decisions_info}\n'
            f'{target_info}'
            f'{algorithm_info}'
            f'{framework_info}'
            f'{fall_back_info}'
            f'{missing_value_encodings_info}'
            f'{data_type_version_info}'
            f'  misc:\n'
            f'{misc_info}'
        )

    def validate(self) -> None:
        sanitized_name_dict: Dict[str, Any] = dict()
        validate_sanitized_names(self.inputs, sanitized_name_dict)
        validate_sanitized_names(self.outputs, sanitized_name_dict)
        validate_sanitized_names(self.targets, sanitized_name_dict)
        validate_sanitized_names(self.metadata, sanitized_name_dict)  # type: ignore
        validate_sanitized_names(self.decisions, sanitized_name_dict)  # type: ignore

    def get_all_cols(self) -> List[Column]:
        result = copy.deepcopy(self.inputs)
        if self.outputs is not None:
            result += self.outputs
        if self.metadata is not None:
            result += self.metadata
        if self.decisions is not None:
            result += self.decisions
        if self.targets is not None:
            result += self.targets
        return result

    def get_col(self, col_name: str) -> Union[Column, None]:
        for col in self.get_all_cols():
            if col.name == col_name:
                return col
        return None


CURRENT_SCHEMA_VERSION = 0.1
DEFUNCT_MODELINFO_SCHEMA_VERSION = '0.0'
CURRENT_MODELINFO_SCHEMA_VERSION = '1.2'
VALID_OPERATORS = ['==', '>=', '<=', '>', '<']


def _summary_dataframe_for_columns(
    columns: Sequence[Column], placeholder: str = ''
) -> pd.DataFrame:
    """
        Example:
                 column     dtype count(possible_values) is_nullable            value_range
    0       CreditScore   INTEGER                              False        376 - 850
    1         Geography  CATEGORY                      3       False
    2            Gender  CATEGORY                      2       False
    3               Age   INTEGER                              False         18 - 82
    4            Tenure   INTEGER                              False          0 - 10
    5           Balance     FLOAT                              False        0.0 - 213,100.0
    6     NumOfProducts   INTEGER                              False          1 - 4
    7         HasCrCard  CATEGORY                      2       False
    8    IsActiveMember  CATEGORY                      2       False
    9   EstimatedSalary     FLOAT                              False      371.1 - 199,700.0
    10          Churned  CATEGORY                      2       False

    """  # noqa E501
    column_names = []
    column_dtypes = []
    n_possible_values = []
    is_nullable = []
    mins: List[Any] = []
    maxes: List[Any] = []
    for column in columns:
        column_names.append(column.name)
        column_dtypes.append(column.data_type.name)
        n_possible_values.append(
            len(column.possible_values)
            if column.possible_values is not None
            else placeholder
        )
        is_nullable.append(
            str(column.is_nullable) if column.is_nullable is not None else placeholder
        )
        if not column.data_type.is_numeric():
            mins.append(None)
            maxes.append(None)
        else:
            min_str = (
                prettyprint_number(column.value_range_min)  # type: ignore
                if column.value_range_min is not None
                else '*'
            )
            max_str = (
                prettyprint_number(column.value_range_max)  # type: ignore
                if column.value_range_max is not None
                else '*'
            )
            mins.append(min_str)
            maxes.append(max_str)
    range_pad_len = max(len(x) if x is not None else 0 for x in mins + maxes)
    value_range = [
        (placeholder if x is None else f'{x:>{range_pad_len}} - {y:<{range_pad_len}}')
        for x, y in zip(mins, maxes)
    ]
    return pd.DataFrame(
        {
            'column': column_names,
            'dtype': column_dtypes,
            'count(possible_values)': n_possible_values,
            'is_nullable': is_nullable,
            'value_range': value_range,
        }
    )


def _summary_dataframe_for_custom_features(
    custom_features: Sequence[CustomFeature],
) -> pd.DataFrame:
    """
        Example:
        name    column                      type                transformation  n_clusters  monitor  monitor_components
    0   F1      'col_name1'                 FROM_TEXT           'Word2vec'      3           True        False
    1   F2      ['col_name2','col_name3']   FROM_COLUMNS        None            4           True        False
    2   F3      'col_name4'                 FROM_VECTOR         None            auto        True        False
    3   F4      'col_name5'                 FROM_DICTIONARY     None            auto        True        False
    """  # noqa E501
    names = []
    columns = []
    types = []
    clusters: List[Any] = []
    source_columns = []
    embeddings = []

    for feature in custom_features:
        names.append(feature.name)
        types.append(feature.type.name)
        columns.append(feature.column)
        source_columns.append(feature.source_column)
        embeddings.append(feature.column)

        if feature.n_clusters is not None:
            clusters.append(feature.n_clusters)
        else:
            clusters.append('auto')

    return pd.DataFrame(
        {
            'name': names,
            'type': types,
            'column': columns,
            'source': source_columns,
            'embeddings': embeddings,
            'n_clusters': clusters,
        }
    )


@enum.unique
class BaselineType(str, enum.Enum):
    PRE_PRODUCTION = 'PRE_PRODUCTION'
    STATIC_PRODUCTION = 'STATIC_PRODUCTION'
    ROLLING_PRODUCTION = 'ROLLING_PRODUCTION'

    def __str__(self) -> str:
        return self.value


@enum.unique
class WindowSize(enum.IntEnum):
    FIVE_MINUTES = 300
    ONE_HOUR = 3600
    ONE_DAY = 86400
    ONE_WEEK = 604800
    ONE_MONTH = 2592000

    def __str__(self) -> str:
        return self.name
