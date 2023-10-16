from __future__ import annotations

import json
import os
import tempfile
import time
from http import HTTPStatus
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd
import yaml

from fiddler.api.helpers import multipart_upload
from fiddler.constants import FileType, UploadType
from fiddler.core_objects import DatasetInfo
from fiddler.exceptions import HttpException
from fiddler.libs.http_client import RequestClient
from fiddler.schema.dataset import Dataset, DatasetIngest
from fiddler.schema.server_info import ServerInfo
from fiddler.utils.decorators import handle_api_error_response
from fiddler.utils.helpers import match_semver
from fiddler.utils.logger import get_logger
from fiddler.utils.response_handler import (
    APIResponseHandler,
    PaginatedResponseHandler,
)
from fiddler.validators.dataset_validator import (
    validate_dataset_columns,
    validate_dataset_info,
    validate_dataset_shape,
)

DEFAULT_NROWS_PER_CHUNK = 100000
DEFAULT_SAMPLE_SIZE = 20000
logger = get_logger(__name__)


class DatasetMixin:
    client: RequestClient
    organization_name: str
    server_info: ServerInfo

    @handle_api_error_response
    def get_datasets(self, project_id: str) -> List[Dataset]:
        """
        Get all the datasets in a project

        :param project_id:      The project for which you want to get the datasets
        :returns:               A list containing `Dataset` objects.
        """
        response = self.client.get(
            url='datasets',
            params={
                'organization_name': self.organization_name,
                'project_name': project_id,
            },
        )
        items = PaginatedResponseHandler(response).get_pagination_items()
        datasets = [Dataset.from_dict(item) for item in items]
        return datasets

    @handle_api_error_response
    def get_dataset_names(self, project_id: str) -> List[str]:
        """List the names of all datasets in the organization.

        :param project_id: The project name for which you want to get the datasets
        :returns: List of strings containing the names of each dataset.
        """
        datasets = self.get_datasets(project_id=project_id)
        return [dataset.name for dataset in datasets]

    @handle_api_error_response
    def get_dataset(self, project_id: str, dataset_id: str) -> Dataset:
        """
        Get all the details for a given dataset

        :param project_id:    The project name to which the dataset belongs to
        :param dataset_id:    The dataset name of which you need the details

        :returns: Dataset object which contains the details
        """

        response = self.client.get(
            url=f'datasets/{self.organization_name}:{project_id}:{dataset_id}',
        )
        response_handler = APIResponseHandler(response)
        return Dataset.deserialize(response_handler)

    @handle_api_error_response
    def list_datasets(self, project_id: str) -> List[str]:
        """
        List the names of all datasets in the organization.

        :param project_id: The project name for which you want to get the datasets
        :returns: List of strings containing the names of each dataset.
        """

        return self.get_dataset_names(project_id=project_id)

    @handle_api_error_response
    def get_dataset_info(
        self,
        project_id: str,
        dataset_id: str,
    ) -> DatasetInfo:
        """
        Get DatasetInfo for a dataset.

        :param project_id:    The project name to which the dataset belongs to
        :param dataset_id:    The dataset name of which you need the details

        :returns: A fiddler.DatasetInfo object describing the dataset.
        """

        dataset = self.get_dataset(project_id, dataset_id)
        return dataset.info

    @handle_api_error_response
    def add_dataset(
        self,
        name: str,
        project_id: str,
        info: Optional[DatasetInfo] = None,
    ) -> Dataset:
        request_body = dict(
            name=name,
            project_name=project_id,
            organization_name=self.organization_name,
            info=info,
        )

        response = self.client.post(
            url='datasets',
            data=request_body,
        )
        logger.info(f'{name} dataset created')
        return Dataset.deserialize(APIResponseHandler(response))

    @handle_api_error_response
    def delete_dataset(
        self,
        project_id: str,
        dataset_id: str,
    ) -> None:
        """
        Delete a dataset

        :param project_id:    The project name to which the dataset belongs to
        :param dataset_id:    The dataset name of which you need the details

        :returns: None
        """

        response = self.client.delete(
            url=f'datasets/{self.organization_name}:{project_id}:{dataset_id}',
        )
        if response.status_code == HTTPStatus.OK:
            logger.info(f'{dataset_id} deleted successfully.')
        else:
            # @TODO: Handle non 200 status response
            logger.info('Delete unsuccessful')

    @handle_api_error_response
    def upload_dataset_from_file(
        self,
        project_id: str,
        dataset_id: str,
        file_path: Optional[Union[str, Path]] = None,
        file_type: Optional[FileType] = FileType.CSV,
        file_schema: Optional[Dict[str, Any]] = None,
        info: DatasetInfo | None = None,
        size_check_enabled: bool = False,
        files: Dict[str, Any] | None = None,
        is_sync: Optional[bool] = True,
    ) -> Dict[str, str]:
        """
        Upload a dataset.

        :param project_id:    The project to which the dataset belongs to
        :param dataset_id:    The dataset name of which you need the details
        :param file_path:      The file path of file to be  uploaded
        :param size_check_enabled: Deprecated
        :param files:          A dictionary of file name and key and file path as value.
                               Eg `{'train': pathlib.Path('datasets/train.csv')}`
        :param info:           DatasetInfo object
        :param file_type:      FileType which specifices the filetype csv etc.
        :param file_schema:    <TBD>
        :param is_sync:        A boolean value which determines if the upload method
                               works in synchronous mode or async mode

        :returns:              Dictionary containing details of the job used to publish
                               events incase of 202 response from the server.
        """

        # Remove while removing compatibility
        if file_path and files is None:
            if type(file_path) is not Path:
                file_path = Path(file_path)
            file_name = os.path.basename(file_path).split('.')[0]
            files = {file_name: file_path}
        validate_dataset_info(info)  # type: ignore
        validate_dataset_shape(files)  # type: ignore

        file_names = []
        for _, file_path in files.items():  # type: ignore
            _, file_name = os.path.split(file_path)  # type: ignore
            validate_dataset_columns(info, file_path)  # type: ignore
            response = multipart_upload(
                client=self.client,
                organization_name=self.organization_name,
                project_name=project_id,
                identifier=dataset_id,
                upload_type=UploadType.DATASET.value,
                file_path=str(file_path),
                file_name=file_name,
            )
            file_names.append(response.get('file_name'))

        request_body = DatasetIngest(
            name=dataset_id,
            file_name=file_names,
            info=info,
            file_type=file_type,
            file_schema=file_schema,
        ).to_dict()
        response = self.client.post(
            url=f'datasets/{self.organization_name}:{project_id}:{dataset_id}/ingest',
            data=json.dumps(request_body),  # type: ignore
        )
        # @TODO: Handle invalid file path exception
        if response.status_code == HTTPStatus.ACCEPTED:
            resp = APIResponseHandler(response).get_data()
            if is_sync:
                job_uuid = resp['job_uuid']
                job_name = f'Dataset[{project_id}/{dataset_id}] - Upload dataset'
                logger.info(
                    'Dataset[%s/%s] - Submitted job (%s) for uploading dataset',
                    project_id,
                    dataset_id,
                    job_uuid,
                )

                job = self.wait_for_job(uuid=job_uuid, job_name=job_name).get_data()  # type: ignore
                job.pop('extras', None)
                time.sleep(20)
                return job
            else:
                return resp
        else:
            # raising a generic HttpException
            logger.error(f'Failed to upload dataset {dataset_id}.')
            raise HttpException(
                response.status_code,
                error_code=response.status_code,
                message=f'{response.content.decode("utf-8")}',
                errors=[],
            )

    @handle_api_error_response
    def upload_dataset_from_csv(
        self,
        project_id: str,
        dataset_id: str,
        files: Dict[str, Path],
        info: DatasetInfo,
        file_schema: Optional[dict] = None,
        is_sync: Optional[bool] = True,
    ) -> Dict[str, str]:
        """
        Upload dataset as csv file

        :param project_id:    The project to which the dataset belongs to
        :param dataset_id:    Dataset name used for upload
        :param files:           A dictionary of pathlib.Path as value and name as key. Eg `{'train': pathlib.Path('datasets/train.csv')}`
        :param info:            DatasetInfo object
        :param file_schema:    <TBD>
        :param is_sync:         A boolean value which determines if the upload method works in synchronous mode or async mode

        :returns:               Dictionary containing details of the job used to publish events incase of 202 response from the server.
        """
        if not files:
            raise ValueError('`files` is empty. Please enter a valid input')

        return self.upload_dataset_from_file(
            project_id=project_id,
            dataset_id=dataset_id,
            files=files,
            info=info,
            file_type=FileType.CSV,
            file_schema=file_schema,
            is_sync=is_sync,
        )

    @handle_api_error_response
    def upload_dataset(
        self,
        project_id: str,
        dataset: Dict[str, pd.DataFrame],
        dataset_id: str,
        info: Optional[DatasetInfo] = None,
        size_check_enabled: bool = True,
        is_sync: Optional[bool] = True,
    ) -> Dict[str, str]:
        """
        Upload dataset as pd.DataFrame

        :param project_id:    The project to which the dataset belongs to
        :param dataset_id:    The dataset name of which you need the details
        :param dataset:        A dictionary of dataframe as value and name as key. Eg `{'train': train_df}`
        :param info:            DatasetInfo object
        :param size_check_enabled: Deprecated
        :param is_sync:         A boolean value which determines if the upload method works in synchronous mode or async mode

        :returns:               Dictionary containing details of the job used to publish events incase of 202 response from the server.
        """

        if not dataset:
            raise ValueError(f'`datasets` cannot be empty.')

        # will throw HttpException if project does not exist
        self.client.get(url=f'projects/{self.organization_name}:{project_id}')

        with tempfile.TemporaryDirectory() as tmp:
            files = {}
            file_type = FileType.CSV
            if self.server_info and match_semver(
                self.server_info.server_version, '>=23.4.0'
            ):
                file_type = FileType.PARQUET
                for name, df in dataset.items():
                    file_path = Path(tmp) / f'{name}{file_type.value}'
                    try:
                        df.to_parquet(file_path, index=False)
                    except Exception as e:
                        logger.exception(
                            'Failed to convert dataset dataframe to parquet format. Retrying as a CSV file.'
                        )
                        file_type = FileType.CSV
                        files = {}
                        break
                    files[name] = file_path
            if file_type == FileType.CSV:
                for name, df in dataset.items():
                    file_path = Path(tmp) / f'{name}{file_type.value}'
                    df.to_csv(file_path, index=False)
                    files[name] = file_path

            return self.upload_dataset_from_file(
                project_id=project_id,
                dataset_id=dataset_id,
                files=files,
                info=info,
                file_type=file_type,
                is_sync=is_sync,
            )

    @handle_api_error_response
    def upload_dataset_from_dir(
        self,
        project_id: str,
        dataset_id: str,
        dataset_dir: Optional[Path] = None,
        file_type: FileType = FileType.CSV,
        file_schema: Optional[dict] = None,
        size_check_enabled: bool = False,
        is_sync: bool = True,
    ) -> Dict[str, str]:
        """
        Upload dataset artefacts (data file and dataset info yaml) from a directory

        :param project_id:    The project to which the dataset belongs to
        :param dataset_id:    The dataset name of which you need the details
        :param dataset_dir:     pathlib.Path pointing to the dataset dir to be uploaded
        :param file_type:       FileType
        :param file_schema:     <TBD>
        :param size_check_enabled: Deprecated
        :param is_sync:         A boolean value which determines if the upload method works in synchronous mode or async mode

        :returns:               Dictionary containing details of the job used to publish events incase of 202 response from the server.
        """
        # @TODO: Move repetative input validation used accross different methods to utils

        if file_type != FileType.CSV:
            raise NotImplementedError('Only CSV filetype is supported')

        if not dataset_dir.is_dir():  # type: ignore
            raise ValueError(f'{dataset_dir} is not a directory')

        files = {
            data_file.name: data_file
            for data_file in dataset_dir.glob(f'*{file_type.value}')  # type: ignore
        }

        if not files:
            raise ValueError(f'No data files found in {dataset_dir}.')

        info_yaml = dataset_dir / f'{dataset_id}.yaml'  # type: ignore

        if not info_yaml.exists():
            raise ValueError(f'DatasetInfo yaml ({info_yaml}) not found.')

        with open(info_yaml) as f:
            info = DatasetInfo.from_dict(yaml.safe_load(f))

        return self.upload_dataset_from_file(
            project_id=project_id,
            dataset_id=dataset_id,
            files=files,
            info=info,
            file_schema=file_schema,
            is_sync=is_sync,
        )
