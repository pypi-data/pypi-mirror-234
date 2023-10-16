import json
import tempfile
from http import HTTPStatus
from pathlib import Path
from typing import Any, Dict, Optional, Union

import pandas as pd
from requests_toolbelt.multipart.encoder import MultipartEncoder

from fiddler.api.helpers import multipart_upload
from fiddler.constants import FiddlerTimestamp, FileType, UploadType
from fiddler.core_objects import BatchPublishType
from fiddler.exceptions import HttpException
from fiddler.libs.http_client import RequestClient
from fiddler.schema.events import EventIngest, EventsIngest
from fiddler.schema.server_info import ServerInfo
from fiddler.utils.decorators import handle_api_error_response
from fiddler.utils.helpers import match_semver
from fiddler.utils.logger import get_logger
from fiddler.utils.response_handler import APIResponseHandler

logger = get_logger(__name__)


class EventsMixin:
    client: RequestClient
    organization_name: str
    server_info: ServerInfo

    @handle_api_error_response
    def _publish_events_batch_from_file(
        self,
        project_name: str,
        model_name: str,
        events_path: Path,
        batch_id: Optional[str] = None,
        events_schema: Optional[str] = None,
        id_field: Optional[str] = None,
        is_update: Optional[bool] = None,
        timestamp_field: Optional[str] = None,
        timestamp_format: Optional[FiddlerTimestamp] = None,
        group_by: Optional[str] = None,
        file_type: Optional[FileType] = None,
        wait: Optional[bool] = False,
    ) -> Dict[str, str]:
        """
        Publishes a batch events object to Fiddler Service.

        :param project_name: The project to which the model whose events are being published belongs.
        :param model_name: The model whose events are being published.
        :param events_path: pathlib.Path pointing to the events file to be uploaded
        :param batch_id: <TBD>
        :param events_schema: <TBD>
        :param id_field: Column to extract id value from.
        :param is_update: Bool indicating if the events are updates to previously published rows
        :param timestamp_field: Column to extract timestamp value from.
                                Timestamp must match the specified format in `timestamp_format`.
        :param timestamp_format:Format of timestamp within batch object. Can be one of:
                                - FiddlerTimestamp.INFER
                                - FiddlerTimestamp.EPOCH_MILLISECONDS
                                - FiddlerTimestamp.EPOCH_SECONDS
                                - FiddlerTimestamp.ISO_8601
        :param group_by: Column to group events together for Model Performance metrics. For example,
                        in ranking models that column should be query_id or session_id, used to
                        compute NDCG and MAP. Be aware that the batch_source file/dataset provided should have
                        events belonging to the SAME query_id/session_id TOGETHER and cannot be mixed
                        in the file. For example, having a file with rows belonging to query_id 31,31,31,2,2,31,31,31
                        would not work. Please sort the file by group_by group first to have rows with
                        the following order: query_id 31,31,31,31,31,31,2,2.
        :param file_type: FileType which specifies the filetype csv etc.
        :param wait: A boolean value which determines if the upload method works in synchronous mode or async mode
        :returns: Dictionary containing details of the job used to publish events incase of 202 response from the server.
        """

        file_name = events_path.name
        response = multipart_upload(
            client=self.client,
            organization_name=self.organization_name,
            project_name=project_name,
            identifier=model_name,
            upload_type=UploadType.EVENT.value,
            file_path=str(events_path),
            file_name=file_name,
        )
        file_name = response.get('file_name')
        request_body = EventsIngest(
            batch_id=batch_id,
            events_schema=events_schema,
            id_field=id_field,
            is_update=is_update,
            timestamp_field=timestamp_field,
            timestamp_format=timestamp_format,
            group_by=group_by,
            file_type=file_type,
            file_name=[file_name],
        ).dict()
        response = self.client.post(
            url=f'events/{self.organization_name}:{project_name}:{model_name}/ingest',
            data=request_body,
        )
        # @TODO: Handle invalid file path exception
        if response.status_code == HTTPStatus.ACCEPTED:
            resp = APIResponseHandler(response).get_data()
            if wait:
                job_uuid = resp['job_uuid']
                job_name = f'Model[{project_name}/{model_name}] - Publish events batch'
                logger.info(
                    'Model[%s/%s] - Submitted job (%s) for publish events batch',
                    project_name,
                    model_name,
                    job_uuid,
                )

                job = self.wait_for_job(uuid=job_uuid, job_name=job_name).get_data()  # type: ignore
                job.pop('extras', None)
                return job
            else:
                return resp
        else:
            # raising a generic HttpException
            logger.error('Failed to publish events')
            raise HttpException(
                response.status_code,
                error_code=response.status_code,
                message=f'{response.content.decode("utf-8")}',
                errors=[],
            )

    @handle_api_error_response
    def publish_events_batch(
        self,
        project_id: str,
        model_id: str,
        batch_source: Union[pd.DataFrame, str] = None,
        id_field: Optional[str] = None,
        update_event: Optional[bool] = False,
        timestamp_field: Optional[str] = None,
        timestamp_format: FiddlerTimestamp = FiddlerTimestamp.INFER,
        data_source: Optional[BatchPublishType] = None,
        casting_type: Optional[bool] = False,
        credentials: Optional[dict] = None,
        group_by: Optional[str] = None,
        events_path: Optional[Path] = None,
        batch_id: Optional[str] = None,
        events_schema: Optional[str] = None,
        file_type: Optional[FileType] = None,
        wait: Optional[bool] = False,
    ) -> Dict[str, str]:
        """
        Publishes a batch events object to Fiddler Service.

        :param project_id: The project to which the model whose events are being published belongs.
        :param model_id: The model whose events are being published.
        :param batch_source: Deprecated
        :param update_event: Bool indicating if the events are updates to previously published rows
        :param data_source: Deprecated
        :param casting_type: Deprecated
        :param credentials: Deprecated
        :param events_path: pathlib.Path pointing to the events file to be uploaded
        :param batch_id: <TBD>
        :param events_schema: <TBD>
        :param id_field: Column to extract id value from.
        :param timestamp_field: Column to extract timestamp value from.
                                Timestamp must match the specified format in `timestamp_format`.
        :param timestamp_format:Format of timestamp within batch object. Can be one of:
                                - FiddlerTimestamp.INFER
                                - FiddlerTimestamp.EPOCH_MILLISECONDS
                                - FiddlerTimestamp.EPOCH_SECONDS
                                - FiddlerTimestamp.ISO_8601
        :param group_by: Column to group events together for Model Performance metrics. For example,
                        in ranking models that column should be query_id or session_id, used to
                        compute NDCG and MAP. Be aware that the batch_source file/dataset provided should have
                        events belonging to the SAME query_id/session_id TOGETHER and cannot be mixed
                        in the file. For example, having a file with rows belonging to query_id 31,31,31,2,2,31,31,31
                        would not work. Please sort the file by group_by group first to have rows with
                        the following order: query_id 31,31,31,31,31,31,2,2.
        :param file_type: FileType which specifies the filetype csv etc.
        :param wait: A boolean value which determines if the upload method works in synchronous mode or async mode
        :returns: Dictionary containing details of the job used to publish events incase of 202 response from the server.
        """

        # Either batch_source or events_path can be given for _publish_events_batch_from_file
        if batch_source is None and events_path is None:
            raise ValueError(f'`batch_source` parameter is required.')

        if timestamp_format:
            if type(timestamp_format) is not FiddlerTimestamp:
                raise ValueError(
                    f'timestamp_format format is not of type FiddlerTimestamp'
                )
            timestamp_format = FiddlerTimestamp(timestamp_format.value)
        if type(batch_source) == pd.DataFrame and (
            data_source is None or BatchPublishType.DATAFRAME == data_source
        ):
            if batch_source.empty:
                raise ValueError(
                    'The batch provided is empty. Please retry with at least one row of data.'
                )
            return self._publish_events_batch_dataframe(
                project_name=project_id,
                model_name=model_id,
                events_df=batch_source,
                id_field=id_field,
                is_update=update_event,
                timestamp_field=timestamp_field,
                timestamp_format=timestamp_format,
                group_by=group_by,
                wait=wait,
            )
        elif (events_path or type(batch_source) == str) and (
            data_source is None or BatchPublishType.LOCAL_DISK == data_source
        ):
            return self._publish_events_batch_from_file(
                project_name=project_id,
                model_name=model_id,
                events_path=events_path or Path(batch_source),
                id_field=id_field,
                is_update=update_event,
                timestamp_field=timestamp_field,
                timestamp_format=timestamp_format,
                group_by=group_by,
                file_type=file_type,
                wait=wait,
            )
        else:
            raise NotImplementedError(
                'Batch source other than dataframe and csv is not implemented now'
            )

    @handle_api_error_response
    def publish_event(
        self,
        project_id: str,
        model_id: str,
        event: dict,
        event_id: Optional[str] = None,
        update_event: Optional[bool] = None,
        event_timestamp: Optional[int] = None,
        timestamp_format: FiddlerTimestamp = FiddlerTimestamp.INFER,
        casting_type: Optional[bool] = False,
        dry_run: Optional[bool] = False,
        id_field: Optional[str] = None,
    ) -> Optional[str]:
        """
        Publishes an event to Fiddler Service.

        :param project_id: The project to which the model whose events are being published belongs.
        :param model_id: The model whose events are being published.
        :param casting_type: Deprecated
        :param update_event: Bool indicating if the events are updates to previously published rows
        :param dry_run: Deprecated
        :param dict event: Dictionary of event details, such as features and predictions.
        :param event_id: Unique str event id for the event
        :param event_timestamp: The UTC timestamp of the event in epoch milliseconds (e.g. 1609462800000)
        :param timestamp_format: Format of timestamp within batch object. Can be one of:
                                - FiddlerTimestamp.INFER
                                - FiddlerTimestamp.EPOCH_MILLISECONDS
                                - FiddlerTimestamp.EPOCH_SECONDS
                                - FiddlerTimestamp.ISO_8601
        :returns: Unique event id incase of successful submitted request.
        """

        if timestamp_format:
            if type(timestamp_format) is not FiddlerTimestamp:
                raise ValueError(
                    f'timestamp_format format is not of type FiddlerTimestamp'
                )
            timestamp_format = FiddlerTimestamp(timestamp_format.value)

        request_body = EventIngest(
            event=event,
            event_id=event_id,
            id_field=id_field,
            is_update=update_event,
            event_timestamp=event_timestamp,
            timestamp_format=timestamp_format,
        ).dict()
        response = self.client.post(
            url=f'events/{self.organization_name}:{project_id}:{model_id}/ingest/event',
            data=request_body,
        )
        if response.status_code == HTTPStatus.ACCEPTED:
            response_dict = APIResponseHandler(response).get_data()
            logger.info(response_dict.get('message'))
            return response_dict.get('__fiddler_id')
        else:
            # raising a generic HttpException
            logger.error('Failed to publish events')
            raise HttpException(
                response.status_code,
                error_code=response.status_code,
                message=f'{response.content.decode("utf-8")}',
                errors=[],
            )

    @handle_api_error_response
    def _publish_events_batch_dataframe(
        self,
        project_name: str,
        model_name: str,
        events_df: pd.DataFrame,
        batch_id: Optional[str] = None,
        id_field: Optional[str] = None,
        is_update: Optional[bool] = None,
        timestamp_field: Optional[str] = None,
        timestamp_format: Optional[FiddlerTimestamp] = None,
        group_by: Optional[str] = None,
        wait: Optional[bool] = False,
    ) -> Dict[str, str]:
        """
        Publishes a batch events object to Fiddler Service.

        :param project_name: The project to which the model whose events are being published belongs.
        :param model_name: The model whose events are being published.
        :param events_df: pd.DataFrame object having the events
        :param batch_id: <TBD>
        :param id_field: Column to extract id value from.
        :param is_update: Bool indicating if the events are updates to previously published rows
        :param timestamp_field: Column to extract timestamp value from.
                                Timestamp must match the specified format in `timestamp_format`.
        :param timestamp_format: Format of timestamp within batch object. Can be one of:
                                - FiddlerTimestamp.INFER
                                - FiddlerTimestamp.EPOCH_MILLISECONDS
                                - FiddlerTimestamp.EPOCH_SECONDS
                                - FiddlerTimestamp.ISO_8601
        :param group_by: Column to group events together for Model Performance metrics. For example,
                        in ranking models that column should be query_id or session_id, used to
                        compute NDCG and MAP. Be aware that the batch_source file/dataset provided should have
                        events belonging to the SAME query_id/session_id TOGETHER and cannot be mixed
                        in the file. For example, having a file with rows belonging to query_id 31,31,31,2,2,31,31,31
                        would not work. Please sort the file by group_by group first to have rows with
                        the following order: query_id 31,31,31,31,31,31,2,2.
        :param wait: A boolean value which determines if the upload method works in synchronous mode or async mode
        :returns: Dictionary containing details of the job used to publish events incase of 202 response from the server.
        """
        if events_df is None or events_df.empty:
            raise ValueError(
                'The batch provided is empty. Please retry with at least one row of data.'
            )

        file_type = FileType.CSV
        if self.server_info and match_semver(
            self.server_info.server_version, '>=23.4.0'
        ):
            with tempfile.NamedTemporaryFile(suffix=FileType.PARQUET) as temp_file:
                try:
                    events_df.to_parquet(temp_file.name, index=False)
                    return self.publish_events_batch(
                        project_id=project_name,
                        model_id=model_name,
                        batch_source=temp_file.name,
                        batch_id=batch_id,
                        id_field=id_field,
                        update_event=is_update,
                        timestamp_field=timestamp_field,
                        timestamp_format=timestamp_format,
                        group_by=group_by,
                        wait=wait,
                        file_type=FileType.PARQUET,
                    )
                except Exception as e:
                    logger.exception(
                        'Failed to convert events dataframe to parquet format. Retrying as a CSV file.'
                    )
        with tempfile.NamedTemporaryFile(suffix=file_type) as temp_file:
            events_df.to_csv(temp_file.name, index=False)
            return self.publish_events_batch(
                project_id=project_name,
                model_id=model_name,
                batch_source=temp_file.name,
                batch_id=batch_id,
                id_field=id_field,
                update_event=is_update,
                timestamp_field=timestamp_field,
                timestamp_format=timestamp_format,
                group_by=group_by,
                wait=wait,
                file_type=file_type,
            )

    @handle_api_error_response
    def publish_events_batch_schema(  # noqa
        self,
        batch_source: Union[Path, str],
        publish_schema: Dict[str, Any],
        data_source: Optional[BatchPublishType] = None,
        wait: Optional[bool] = False,
    ) -> Dict[str, str]:
        """
        Publishes a batch events object to Fiddler Service.

        :param batch_source: pathlib.Path pointing to the events file to be uploaded
        :param publish_schema: Dict object specifying layout of data.
        :param data_source: path of the source file of type BatchPublishType
        :param wait: A boolean value which determines if the upload method works in
                        synchronous mode or async mode
        :returns: Dictionary containing details of the job used to publish events incase
                  of 202 response from the server.
        """
        request_body_json = {}
        request_body_json['schema'] = publish_schema
        request_body: Dict[str, Any] = {}
        if data_source == BatchPublishType.AWS_S3 and isinstance(batch_source, str):
            request_body.update(
                {
                    's3_url': batch_source,
                    'schema': json.dumps(publish_schema),
                }
            )
            response = self.client.post(
                url=f'events/{self.organization_name}/ingest/schema',
                headers={'Content-Type': 'application/json'},
                data=request_body,
            )
        else:
            if isinstance(batch_source, str):
                batch_source = Path(batch_source)
            file_name = batch_source.name
            files = {}
            files[file_name] = batch_source
            request_body.update(
                {
                    file_path.name: (
                        file_path.name,
                        open(file_path, 'rb'),
                    )
                    for _, file_path in files.items()
                }
            )
            # https://stackoverflow.com/a/19105672/13201804
            request_body.update(
                {'schema': (None, json.dumps(publish_schema), 'application/json')}
            )
            m = MultipartEncoder(fields=request_body)
            content_type_header, request_body = m.content_type, m
            # content_type_header, request_body  = event_ingest.multipart_form_request()
            response = self.client.post(
                url=f'events/{self.organization_name}/ingest/schema',
                headers={'Content-Type': content_type_header},
                data=request_body,
            )
        # @TODO: Handle invalid file path exception
        if response.status_code == HTTPStatus.ACCEPTED:
            resp = APIResponseHandler(response).get_data()
            if wait:
                job_uuid = resp['job_uuid']
                project_name = publish_schema.get('__static', {}).get('__project')
                model_name = publish_schema.get('__static', {}).get('__model')
                job_name = (
                    f'Model[{project_name}/{model_name}] - Publish events batch schema',
                )

                logger.info(
                    'Model[%s/%s]: Submitted job (%s) for publish events batch schema',
                    project_name,
                    model_name,
                    job_uuid,
                )
                job = self.wait_for_job(uuid=job_uuid, job_name=job_name).get_data()  # type: ignore
                job.pop('extras', None)
                return job
            else:
                return resp

        else:
            # raising a generic HttpException
            logger.error('Failed to upload events schema.')
            raise HttpException(
                response.status_code,
                error_code=response.status_code,
                message=f'{response.content.decode("utf-8")}',
                errors=[],
            )
