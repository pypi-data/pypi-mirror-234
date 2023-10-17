import logging
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from fiddler.connection import Connection
from fiddler.file_processor.src.constants import PARQUET_EXTENSION

from ..aws_utils import validate_gcp_uri_access, validate_s3_uri_access
from ..core_objects import BatchPublishType, FiddlerTimestamp
from ..utils.formatting import formatted_utcnow, print_streamed_result
from ..utils.helper import infer_data_source
from ..utils.pandas import clean_df_types, write_dataframe_to_parquet_file

LOG = logging.getLogger(__name__)


class PublishEvent:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def _publish_event_batch(
        self,
        req_path: List[str],
        req_payload: Dict[str, Any],
        batch_source: Union[pd.DataFrame, str],
        data_source: Optional[BatchPublishType] = None,
        credentials: Optional[dict] = None,
    ):
        if data_source is None:
            data_source = infer_data_source(source=batch_source)
            LOG.info(
                f'`data_source` not specified. Inferred `data_source` as '
                f'BatchPublishType.{BatchPublishType(data_source.value).name}'
            )

        if data_source not in BatchPublishType:
            raise ValueError('Please specify a valid batch_source')

        assert data_source is not None, 'data_source unexpectedly None'

        req_payload['data_source'] = data_source.value

        if data_source == BatchPublishType.DATAFRAME:
            # Converting dataframe to local disk format for transmission
            req_payload['data_source'] = BatchPublishType.LOCAL_DISK.value

            assert isinstance(
                batch_source, pd.DataFrame
            ), 'batch_source unexpectedly not a DataFrame'

            if batch_source.empty:
                raise ValueError(
                    'The batch provided is empty. Please retry with at least one row of data.'
                )

            df = batch_source.copy()
            if df.index.name is not None:
                df.reset_index(inplace=True)

            clean_df_types(df)

            with tempfile.TemporaryDirectory() as tmp_dir:
                file_path = Path(tmp_dir) / f'log.{PARQUET_EXTENSION}'

                write_dataframe_to_parquet_file(df=df, file_path=file_path)

                result = self.connection.call(
                    path=req_path,
                    json_payload=req_payload,
                    files=[file_path],
                    stream=True,
                )

        elif data_source == BatchPublishType.LOCAL_DISK:
            local_file_path = batch_source
            result = self.connection.call(
                path=req_path,
                json_payload=req_payload,
                files=[Path(local_file_path)],
                stream=True,
            )

        elif data_source == BatchPublishType.AWS_S3:
            s3_uri = batch_source
            # Validate S3 credentials
            validate_s3_uri_access(s3_uri, credentials, throw_error=True)
            with tempfile.NamedTemporaryFile() as tmp:
                # tmp is a dummy file passed to BE for ease of API consolidation
                req_payload['file_path'] = s3_uri
                req_payload['credentials'] = credentials
                result = self.connection.call(
                    path=req_path,
                    json_payload=req_payload,
                    files=[Path(tmp.name)],
                    stream=True,
                )

        elif data_source == BatchPublishType.GCP_STORAGE:
            gcp_uri = batch_source
            # Validate GCS credentials
            gcs_credentials: Optional[Dict[str, Any]] = None
            if credentials is not None:
                gcs_credentials = {}
                if 'gcs_access_key_id' in credentials:
                    gcs_credentials['aws_access_key_id'] = credentials[
                        'gcs_access_key_id'
                    ]
                if 'gcs_secret_access_key' in credentials:
                    gcs_credentials['aws_secret_access_key'] = credentials[
                        'gcs_secret_access_key'
                    ]
                if 'gcs_session_token' in credentials:
                    gcs_credentials['aws_session_token'] = credentials[
                        'gcs_session_token'
                    ]

            validate_gcp_uri_access(gcp_uri, gcs_credentials, throw_error=True)
            with tempfile.NamedTemporaryFile() as tmp:
                # tmp is a dummy file passed to BE for ease of API consolidation
                req_payload['file_path'] = gcp_uri
                req_payload['credentials'] = gcs_credentials
                result = self.connection.call(
                    path=req_path,
                    json_payload=req_payload,
                    files=[Path(tmp.name)],
                    stream=True,
                )
        else:
            raise ValueError(f'Data source {data_source} not supported')

        final_return = None
        for res in result:
            print_streamed_result(res)
            final_return = res

        return final_return

    def publish_events_batch(  # noqa
        self,
        project_id: str,
        model_id: str,
        batch_source: Union[pd.DataFrame, str],
        id_field: Optional[str] = None,
        update_event: Optional[bool] = False,
        timestamp_field: Optional[str] = None,
        timestamp_format: FiddlerTimestamp = FiddlerTimestamp.INFER,
        data_source: Optional[BatchPublishType] = None,
        casting_type: Optional[bool] = False,
        credentials: Optional[dict] = None,
        group_by: Optional[str] = None,
    ):
        """
        Publishes a batch events object to Fiddler Service.
        :param project_id:    The project to which the model whose events are being published belongs.
        :param model_id:      The model whose events are being published.
        :param batch_source:  Batch object to be published. Can be one of: Pandas DataFrame, CSV file, PKL Pandas DataFrame, or Parquet file.
        :param id_field:  Column to extract id value from.
        :param update_event: Bool indicating if the events are updates to previously published rows
        :param timestamp_field:     Column to extract timestamp value from.
                              Timestamp must match the specified format in `timestamp_format`.
        :param timestamp_format:   Format of timestamp within batch object. Can be one of:
                                - FiddlerTimestamp.INFER
                                - FiddlerTimestamp.EPOCH_MILLISECONDS
                                - FiddlerTimestamp.EPOCH_SECONDS
                                - FiddlerTimestamp.ISO_8601
        :param data_source:   Source of batch object. In case of failed inference, can be one of:
                                - BatchPublishType.DATAFRAME
                                - BatchPublishType.LOCAL_DISK
                                - BatchPublishType.AWS_S3
                                - BatchPublishType.GCP_STORAGE
        :param casting_type: Bool indicating if fiddler should try to cast the data in the event with
                             the type referenced in model info. Default to False.
        :param credentials:  Dictionary containing authorization for AWS or GCP.

                             For AWS S3, list of expected keys are
                              ['aws_access_key_id', 'aws_secret_access_key', 'aws_session_token']
                              with 'aws_session_token' being applicable to the AWS account being used.

                             For GCP, list of expected keys are
                              ['gcs_access_key_id', 'gcs_secret_access_key', 'gcs_session_token']
                              with 'gcs_session_token' being applicable to the GCP account being used.
        :param group_by: Column to group events together for Model Performance metrics. For example,
                         in ranking models that column should be query_id or session_id, used to
                         compute NDCG and MAP. Be aware that the batch_source file/dataset provided should have
                         events belonging to the SAME query_id/session_id TOGETHER and cannot be mixed
                         in the file. For example, having a file with rows belonging to query_id 31,31,31,2,2,31,31,31
                         would not work. Please sort the file by group_by group first to have rows with
                         the following order: query_id 31,31,31,31,31,31,2,2.
        """

        if not timestamp_format or timestamp_format not in FiddlerTimestamp:
            raise ValueError('Please specify a valid timestamp_format')

        assert timestamp_format is not None, 'timestamp_format unexpectedly None'

        path = ['publish_events_batch', self.connection.org_id, project_id, model_id]
        payload: Dict[str, Any] = {
            'casting_type': casting_type,
            'is_update_event': update_event,
            'timestamp_format': timestamp_format.value,
        }

        if id_field is not None:
            payload['id_field'] = id_field
        if timestamp_field is not None:
            payload['timestamp_field'] = timestamp_field
        if group_by is not None:
            payload['group_by'] = group_by

        # Default to current time for case when no timestamp field specified
        if timestamp_field is None:
            curr_timestamp = formatted_utcnow(
                milliseconds=int(round(time.time() * 1000))
            )
            LOG.info(
                f'`timestamp_field` not specified. Using current UTC time `{curr_timestamp}` as default'
            )
            payload['default_timestamp'] = curr_timestamp

        return self._publish_event_batch(
            req_path=path,
            req_payload=payload,
            batch_source=batch_source,
            data_source=data_source,
            credentials=credentials,
        )

    def publish_events_batch_schema(  # noqa
        self,
        batch_source: Union[pd.DataFrame, str],
        publish_schema: Dict[str, Any],
        data_source: Optional[BatchPublishType] = None,
        credentials: Optional[dict] = None,
        group_by: Optional[str] = None,
    ):
        """
        Publishes a batch events object to Fiddler Service.
        :param batch_source:  Batch object to be published. Can be one of: Pandas DataFrame, CSV file, PKL Pandas DataFrame, or Parquet file.
        :param publish_schema: Dict object specifying layout of data.
        :param data_source:   Source of batch object. In case of failed inference, can be one of:
                                - BatchPublishType.DATAFRAME
                                - BatchPublishType.LOCAL_DISK
                                - BatchPublishType.AWS_S3
                                - BatchPublishType.GCP_STORAGE
        :param credentials:  Dictionary containing authorization for AWS or GCP.

                             For AWS S3, list of expected keys are
                              ['aws_access_key_id', 'aws_secret_access_key', 'aws_session_token']
                              with 'aws_session_token' being applicable to the AWS account being used.

                             For GCP, list of expected keys are
                              ['gcs_access_key_id', 'gcs_secret_access_key', 'gcs_session_token']
                              with 'gcs_session_token' being applicable to the GCP account being used.
        :param group_by: Column to group events together for Model Performance metrics. For example,
                         in ranking models that column should be query_id or session_id, used to
                         compute NDCG and MAP.
        """

        path = ['publish_events_batch_schema', self.connection.org_id]
        payload = {
            'publish_schema': publish_schema,
            'group_by': group_by,
        }

        return self._publish_event_batch(
            req_path=path,
            req_payload=payload,
            batch_source=batch_source,
            data_source=data_source,
            credentials=credentials,
        )
