import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from pydantic import parse_obj_as

from fiddler.libs.http_client import RequestClient
from fiddler.utils import logging
from fiddler.v2.schema.alert import (
    AlertCondition,
    AlertRule,
    AlertRulePayload,
    AlertType,
    BinSize,
    ComparePeriod,
    CompareTo,
    Metric,
    Priority,
    TriggeredAlerts,
)
from fiddler.v2.utils.exceptions import handle_api_error_response
from fiddler.v2.utils.helpers import match_semvar
from fiddler.v2.utils.response_handler import (
    APIResponseHandler,
    PaginatedResponseHandler,
)

logger = logging.getLogger(__name__)


class AlertMixin:
    FILTER_ALERT_RULES_API_VERSION = '>=23.1.0'
    GROUP_OF_COLUMNS_API_VERSION = '>=23.3.0'
    GROUP_OF_COLUMNS_LIST_API_VERSION = '>=23.4.0'

    client: RequestClient
    organization_name: str

    @handle_api_error_response
    def add_alert_rule(
        self,
        name: str,
        project_id: str,
        model_id: str,
        alert_type: AlertType,
        metric: Metric,
        compare_to: CompareTo,
        priority: Priority,
        critical_threshold: float,
        condition: AlertCondition,
        bin_size: BinSize = BinSize.ONE_DAY,
        baseline_id: Optional[str] = None,
        compare_period: Optional[ComparePeriod] = None,
        column: Optional[str] = None,
        columns: Optional[List[str]] = None,
        warning_threshold: Optional[float] = None,
        notifications_config: Optional[Dict[str, Dict[str, Any]]] = None,
    ) -> AlertRule:
        """
        To add an alert rule
        :param project_id: Unique project name for which the alert rule is created
        :param model_id: Unique model name for which the alert rule is created
        :param name: Name of the Alert rule
        :param alert_type: Selects one of the four metric types:
                1) AlertType.PERFORMANCE
                2) AlertType.DATA_DRIFT
                3) AlertType.DATA_INTEGRITY
                4) AlertType.SERVICE_METRICS


        :param metric: "metric":
                For service_metrics:
                1) MetricType.TRAFFIC

                For performance:
                1)  For binary_classfication:
                        a) MetricType.ACCURACY b) MetricType.TPR c) MetricType.FPR d) MetricType.PRECISION e) MetricType.RECALL
                        f) MetricType.F1_SCORE g) MetricType.ECE h) MetricType.AUC
                2)  For Regression:
                        a) MetricType.R2 b) MetricType.MSE c) MetricType.MAE d) MetricType.MAPE e) MetricType.WMAPE
                3)  For Multi-class:
                        a) MetricType.ACCURACY b) MetricType.LOG_LOSS
                4) For Ranking:
                        a) MetricType.MAP b) MetricType.MEAN_NDCG

                For drift:
                    1) MetricType.PSI
                    2) MetricType.JSD

                For data_integrity:
                    1) MetricType.RANGE_VIOLATION
                    2) MetricType.MISSING_VALUE
                    3) MetricType.TYPE_VIOLATION
        :param bin_size: bin_size
                Possible Values:
                    1) BinSize.ONE_HOUR
                    2) BinSize.ONE_DAY
                    3) BinSize.SEVEN_DAYS
                    4) BinSize.ONE_MONTH
        :param compare_to: Select from the two:
                1) CompareTo.RAW_VALUE
                2) CompareTo.TIME_PERIOD
        :param compare_period: Comparing with a previous time period. Possible values:
                1) ComparePeriod.ONE_DAY
                2) ComparePeriod.SEVEN_DAYS
                3) ComparePeriod.ONE_MONTH
                4) ComparePeriod.THREE_MONTHS
        :param priority: To set the priority for the alert rule. Select from:
                1) Priority.LOW
                2) Priority.MEDIUM
                3) Priority.HIGH
        :param warning_threshold: Threshold value to crossing which a warning level severity alert will be triggered
        :param critical_threshold: Threshold value to crossing which a critical level severity alert will be triggered
        :param condition: Select from:
                1) AlertCondition.LESSER
                2) AlertCondition.GREATER
        :param column: column name on which alert rule is to be created. It can take '__ANY__' to check for all columns
            Supported by server version 23.2.0 or lower.
        :param columns: List of column names on which alert rule is to be created. It can take ['__ANY__'] to check for all columns.
            Supported by server version 23.3.0 onwards.
        :param notifications_config: notifications config object created using helper method build_notifications_config()
        :param baseline_id: Name of the baselne, whose histogram is compared against the same derived from current data.
                            Used only when alert type is AlertType.DATA_DRIFT.
        :return: created alert rule object
        """

        if not notifications_config:
            notifications_config = self.build_notifications_config()

        if bin_size not in BinSize.keys():
            raise ValueError(f'bin_size: {bin_size} should be one of: {BinSize.keys()}')
        if compare_to == CompareTo.TIME_PERIOD and not compare_period:
            raise ValueError(
                f'compare_period is required when compare_to is {CompareTo.TIME_PERIOD}'
            )
        if compare_period and compare_period not in ComparePeriod.keys():
            raise ValueError(f'compare_period should be one of{ComparePeriod.keys()}')

        alert_rule_payload = AlertRulePayload(
            organization_name=self.organization_name,
            project_name=project_id,
            model_name=model_id,
            name=name,
            alert_type=alert_type,
            metric=metric,
            compare_to=compare_to,
            compare_period=compare_period,
            priority=priority,
            baseline_name=baseline_id,
            warning_threshold=warning_threshold,
            critical_threshold=critical_threshold,
            condition=condition,
            time_bucket=bin_size,
            notifications=notifications_config,
        )
        if match_semvar(self.server_info.server_version, self.GROUP_OF_COLUMNS_API_VERSION):
            if columns:
                if match_semvar(self.server_info.server_version, self.GROUP_OF_COLUMNS_LIST_API_VERSION):
                    alert_rule_payload.feature_names=columns
                else:
                    # version 23.3 support columns is comma separated string
                    alert_rule_payload.feature_names=",".join(columns)
            elif column:
                if match_semvar(self.server_info.server_version, self.GROUP_OF_COLUMNS_LIST_API_VERSION):
                    alert_rule_payload.feature_names=[column]
                else:
                    alert_rule_payload.feature_names=column
        else:
            # we do not support columns in server version < 23.3
            if columns:
                raise ValueError(f'columns is not supported in the server version {self.server_info.server_version}. Please use column instead.')
            if column:
                alert_rule_payload.feature_name=column

        request_body = alert_rule_payload.dict()
        response = self.client.post(
            url='alert-configs',
            data=request_body,
        )
        response_data = APIResponseHandler(response)
        alert_rule_id = response_data.get_data().get('uuid')

        logger.info(f'alert config created with alert_rule_id: {alert_rule_id}')

        return AlertRule.deserialize(response_data)

    @handle_api_error_response
    def delete_alert_rule(self, alert_rule_uuid: str) -> None:
        """
        Delete an alert rule
        :param alert_rule_id: unique id for the alert rule to be deleted
        :return: the response for the delete operation
        """
        self.client.delete(url=f'alert-configs/{alert_rule_uuid}')

        logger.info(
            f'alert config with alert_rule_id: {alert_rule_uuid} deleted successfully.'
        )

    @handle_api_error_response
    def get_alert_rules(
        self,
        project_id: Optional[str] = None,
        model_id: Optional[str] = None,
        alert_type: Optional[AlertType] = None,
        metric: Optional[Metric] = None,
        column: Optional[str] = None,
        columns: Optional[List[str]] = None,
        baseline_id: Optional[str] = None,
        ordering: Optional[List[str]] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> List[AlertRule]:
        """
        Get a list of alert rules with respect to the filtering parameters
        :param project_id: unique project name
        :param model_id: unique model name
        :param alert_type: Selects one of the four metric types:
                1) AlertType.PERFORMANCE
                2) AlertType.DATA_DRIFT
                3) AlertType.DATA_INTEGRITY
                4) AlertType.SERVICE_METRICS
        :param metric: "metric":
                For service_metrics:
                1) MetricType.TRAFFIC

                For performance:
                1)  For binary_classfication:
                        a) MetricType.ACCURACY b) MetricType.TPR c) MetricType.FPR d) MetricType.PRECISION e) MetricType.RECALL
                        f) MetricType.F1_SCORE g) MetricType.ECE h) MetricType.AUC
                2)  For Regression:
                        a) MetricType.R2 b) MetricType.MSE c) MetricType.MAE d) MetricType.MAPE e) MetricType.WMAPE
                3)  For Multi-class:
                        a) MetricType.ACCURACY b) MetricType.LOG_LOSS
                4) For Ranking:
                        a) MetricType.MAP b) MetricType.MEAN_NDCG

                For drift:
                    1) MetricType.PSI
                    2) MetricType.JSD

                For data_integrity:
                    1) MetricType.RANGE_VIOLATION
                    2) MetricType.MISSING_VALUE
                    3) MetricType.TYPE_VIOLATION
        :param column: Filter based on the column
        :param columns: Filter based on a list of column names
        :param limit: Number of records to be retrieved per page, also referred as page_size
        :param offset: Pointer to the starting of the page index. offset of the first page is 0
                        and it increments by limit for each page, for e.g., 5th pages offset when
                        limit=100 will be (5 - 1) * 100 = 400. This means 5th page will contain
                        records from index 400 to 499.
        :return: paginated list of alert rules for the set filters
        """
        alert_params = {
            'organization_name': self.organization_name,
            'offset': offset,
            'limit': limit,
        }

        if match_semvar(
            self.server_info.server_version, self.FILTER_ALERT_RULES_API_VERSION
        ):
            filter_by_rules = []
            if project_id:
                filter_by_rules.append(
                    {'field': 'project_name', 'operator': 'equal', 'value': project_id}
                )

            if model_id:
                filter_by_rules.append(
                    {'field': 'model_name', 'operator': 'equal', 'value': model_id}
                )

            if alert_type:
                filter_by_rules.append(
                    {'field': 'alert_type', 'operator': 'equal', 'value': alert_type}
                )

            if metric:
                filter_by_rules.append(
                    {'field': 'metric', 'operator': 'equal', 'value': metric}
                )

            if match_semvar(self.server_info.server_version, self.GROUP_OF_COLUMNS_API_VERSION):
                if columns:
                    filter_by_rules.append({'field': 'feature_names', 'operator': 'contains', 'value': columns})
                elif column:
                    filter_by_rules.append({'field': 'feature_names', 'operator': 'contains', 'value': [column]})
            else:
                # we do not support columns in server version < 23.3
                if columns:
                    raise ValueError(f'columns is not supported in the server version {self.server_info.server_version}. Please use column instead.')                
                if column:
                    filter_by_rules.append(
                        {'field': 'feature_name', 'operator': 'equal', 'value': column}
                    )
                
            if baseline_id:
                filter_by_rules.append(
                    {
                        'field': 'baseline_name',
                        'operator': 'equal',
                        'value': baseline_id,
                    }
                )

            if ordering:
                alert_params.update({'ordering': ','.join(ordering)})

            alert_params.update(
                {'filter': json.dumps({'condition': 'AND', 'rules': filter_by_rules})}
            )
        else:
            alert_params.update(
                {
                    'project_name': project_id,
                    'model_name': model_id,
                    'alert_type': alert_type,
                    'metric': metric,
                    'feature_name': column,
                    'baseline_name': baseline_id,
                    'ordering': ordering,
                }
            )

        response = self.client.get(
            url='alert-configs',
            params=alert_params,
        )
        _, items = PaginatedResponseHandler(response).get_pagination_details_and_items()

        return parse_obj_as(List[AlertRule], items)

    @handle_api_error_response
    def get_triggered_alerts(
        self,
        alert_rule_uuid: str,
        start_time: datetime = datetime.now() - timedelta(days=7),
        end_time: datetime = datetime.now(),
        ordering: Optional[List[str]] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> List[TriggeredAlerts]:
        """
        To get a list of triggered alerts  for a given alert rule
        :param alert_rule_id: Unique id for the alert rule
        :param start_time: Start time to filter trigger alerts :default: 7 days ago
        :param end_time: End time to filter trigger alerts :default: time now
        :param limit: Number of records to be retrieved per page, also referred as page_size
        :param offset: Pointer to the starting of the page index. offset of the first page is 0
                        and it increments by limit for each page, for e.g., 5th pages offset when
                        limit=100 will be (5 - 1) * 100 = 400. This means 5th page will contain
                        records from index 400 to 499.
        :return: paginated list of triggered_alerts for the given alert rule
        """
        response = self.client.get(
            url=f'alert-configs/{alert_rule_uuid}/records',
            params={
                'organization_name': self.organization_name,
                'start_time': start_time,
                'end_time': end_time,
                'offset': offset,
                'limit': limit,
                'ordering': ordering,
            },
        )
        _, items = PaginatedResponseHandler(response).get_pagination_details_and_items()
        return parse_obj_as(List[TriggeredAlerts], items)

    def build_notifications_config(
        self,
        emails: str = '',
        pagerduty_services: str = '',
        pagerduty_severity: str = '',
    ) -> Dict[str, Dict[str, Any]]:
        """
        To get the notifications value to be set for alert rule
        :param emails: Comma separated emails list
        :param pagerduty_services: Comma separated pagerduty services list
        :param pagerduty severity: Severity for the alerts triggered by pagerduty
        :return: dict with emails and pagerduty dict. If left unused, will store empty string for these values
        """
        return {
            'emails': {
                'email': emails,
            },
            'pagerduty': {
                'service': pagerduty_services,
                'severity': pagerduty_severity,
            },
        }
