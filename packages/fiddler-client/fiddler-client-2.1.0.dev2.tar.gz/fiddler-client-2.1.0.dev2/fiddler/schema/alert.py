import enum
from ast import literal_eval
from typing import Any, Dict, List, Optional, Union

from pydantic import Field, root_validator

from fiddler.schema.base import BaseDataSchema


@enum.unique
class AlertType(str, enum.Enum):
    """Supported Alert types"""

    PERFORMANCE = 'performance'
    DATA_INTEGRITY = 'data_integrity'
    DATA_DRIFT = 'drift'
    SERVICE_METRICS = 'service_metrics'
    STATISTIC = 'statistic'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'


@enum.unique
class Metric(str, enum.Enum):
    """Supported metrics for Alerts."""

    # Drift metrics
    JSD = 'jsd'
    PSI = 'psi'

    ## Data Integrity Metrics
    MISSING_VALUE = 'is_nullable_violation'
    RANGE_VIOLATION = 'is_range_violation'
    TYPE_VIOLATION = 'is_type_violation'

    ## Performance metrics
    # Binary Classification
    ACCURACY = 'accuracy'
    RECALL = 'recall'
    FPR = 'fpr'
    PRECISION = 'precision'
    TPR = 'tpr'
    AUC = 'auc'
    F1_SCORE = 'f1_score'
    ECE = 'expected_callibration_error'

    # Regression
    R2 = 'r2'
    MSE = 'mse'
    MAPE = 'mape'
    WMAPE = 'wmape'
    MAE = 'mae'

    # Multiclass Classification
    LOG_LOSS = 'log_loss'

    # Ranking
    MAP = 'map'
    MEAN_NDCG = 'mean_ndcg'

    ## Service Metrics
    TRAFFIC = 'Traffic'

    ## Statistic
    AVERAGE = 'average'
    SUM = 'sum'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'


@enum.unique
class BinSize(enum.Enum):
    """Bin Size values in millisecs Alerts can be set on"""

    ONE_HOUR = (3600000, 'Hour')
    ONE_DAY = (86400000, 'Day')
    SEVEN_DAYS = (604800000, 'Week')
    ONE_MONTH = (2592000000, 'Month')

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'

    @classmethod
    def keys(cls) -> list:
        return list(cls.__members__.values())


@enum.unique
class ComparePeriod(enum.IntEnum):
    """Time period values for comparison with previous window"""

    ONE_DAY = 86400000
    SEVEN_DAYS = 604800000
    ONE_MONTH = 2592000000
    THREE_MONTHS = 7776000000

    @classmethod
    def keys(cls) -> list:
        return list(cls.__members__.values())

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'


@enum.unique
class CompareTo(str, enum.Enum):
    """Comparison with Absolute(raw_value) or Relative(time_period)"""

    TIME_PERIOD = 'time_period'
    RAW_VALUE = 'raw_value'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'


@enum.unique
class AlertCondition(str, enum.Enum):
    GREATER = 'greater'
    LESSER = 'lesser'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'


@enum.unique
class Priority(str, enum.Enum):
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'


class AlertRulePayload(BaseDataSchema):
    organization_name: str
    project_name: str
    model_name: str
    name: str
    alert_type: Optional[AlertType]
    metric: Union[Metric, str]
    metric_id: Union[Metric, str]
    feature_name: Optional[str]
    feature_names: Optional[List[str]]
    priority: Priority
    compare_to: CompareTo
    baseline_name: Optional[str]
    compare_period: Optional[ComparePeriod]
    warning_threshold: Optional[float]
    critical_threshold: float
    condition: AlertCondition
    time_bucket: int
    bin_size: str
    notifications: Optional[Dict[str, Any]]


class AlertRule(BaseDataSchema):
    alert_rule_uuid: str = Field(alias='uuid')
    organization_name: str
    project_name: str = Field(alias='project_name')
    model_name: str
    name: Optional[str]
    metric: str
    column: Optional[str] = Field(alias='feature_name', default=None)
    columns: Optional[List[str]] = Field(alias='feature_names', default=None)
    baseline_name: Optional[str]
    priority: Priority
    compare_to: CompareTo
    compare_period: Optional[ComparePeriod]
    warning_threshold: Optional[float]
    critical_threshold: float
    condition: AlertCondition
    bin_size: Optional[str]
    time_bucket: Optional[int]
    alert_type_display_name: str
    metric_display_name: str

    @root_validator(pre=True)
    def set_feature_names(cls, values: dict) -> dict:
        if 'feature_names' in values and type(values['feature_names']) == str:
            # in release 23.3 feature_names is stringified list. 23.4 onwards its List[str]
            try:
                values['feature_names'] = literal_eval(values['feature_names'])
            except SyntaxError:
                values['feature_names'] = None
        return values


class TriggeredAlerts(BaseDataSchema):
    id: int
    triggered_alert_id: str = Field(alias='uuid')
    alert_rule_uuid: str = Field(alias='alert_config_uuid')
    alert_run_start_time: int
    alert_time_bucket: int
    alert_value: Union[float, Dict[str, float]]
    baseline_time_bucket: Optional[int]
    baseline_value: Optional[float]
    is_alert: bool
    severity: Optional[str]
    failure_reason: str
    message: str
    multi_col_values: Optional[Dict[str, float]]
    feature_name: Optional[str]
