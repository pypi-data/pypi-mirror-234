"""
Fiddler Client Module
=====================

A Python client for Fiddler service.

TODO: Add Licence.
"""

from fiddler import utils
from fiddler._version import __version__
from fiddler.api import FiddlerApi, FiddlerClient
from fiddler.api.explainability_mixin import (
    DatasetDataSource,
    RowDataSource,
    SqlSliceQueryDataSource,
)
from fiddler.constants import CSV_EXTENSION
from fiddler.core_objects import (
    ArtifactStatus,
    BaselineType,
    BatchPublishType,
    Column,
    DatasetInfo,
    DataType,
    ExplanationMethod,
    FiddlerPublishSchema,
    FiddlerTimestamp,
    ModelInfo,
    ModelInputType,
    ModelTask,
    WeightingParams,
    WindowSize,
)
from fiddler.packtools import gem
from fiddler.schema.alert import (
    AlertCondition,
    AlertType,
    BinSize,
    ComparePeriod,
    CompareTo,
    Metric,
    Priority,
)
from fiddler.schema.model_deployment import DeploymentParams, DeploymentType
from fiddler.schemas.custom_features import (
    CustomFeature,
    ImageEmbedding,
    Multivariate,
    TextEmbedding,
    VectorFeature,
    CustomFeatureType,
)
from fiddler.utils import ColorLogger
from fiddler.utils.logger import get_logger
from fiddler.utils.validator import (
    PackageValidator,
    ValidationChainSettings,
    ValidationModule,
)

logger = get_logger(__name__)

SUPPORTED_API_VERSIONS = ['v2']


__all__ = [
    '__version__',
    'BatchPublishType',
    'Column',
    'CustomFeature',
    'CustomFeatureType',
    'Multivariate',
    'VectorFeature',
    'TextEmbedding',
    'ImageEmbedding',
    'ColorLogger',
    'DatasetInfo',
    'DataType',
    'DeploymentParams',
    'DeploymentType',
    'FiddlerClient',
    'FiddlerApi',
    'FiddlerTimestamp',
    'FiddlerPublishSchema',
    'gem',
    'ModelInfo',
    'ModelInputType',
    'ModelTask',
    'WeightingParams',
    'ExplanationMethod',
    'PackageValidator',
    'ValidationChainSettings',
    'ValidationModule',
    'utils',
    # Exposing constants
    'CSV_EXTENSION',
]
