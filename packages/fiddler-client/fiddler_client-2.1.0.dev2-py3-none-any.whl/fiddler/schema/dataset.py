from __future__ import annotations

from typing import Any, Dict, List, Optional

from fiddler.constants import FileType, UploadType
from fiddler.core_objects import DatasetInfo
from fiddler.exceptions import HttpException
from fiddler.utils.response_handler import APIResponseHandler


class Dataset:
    def __init__(
        self,
        id: int,
        name: str,
        version: str,
        file_list: dict,
        info: DatasetInfo,
        organization_name: str,
        project_name: str,
    ) -> None:
        self.id = id
        self.name = name
        self.version = version
        self.file_list = file_list
        self.info = info
        self.organization_name = organization_name
        self.project_name = project_name

    @classmethod
    def deserialize(cls, response: APIResponseHandler) -> Dataset:
        data = response.get_data()
        try:
            return cls.from_dict(data)
        except KeyError as ke:
            raise HttpException(
                status_code=response.status_code,  # type: ignore
                error_code=response.status_code,  # type: ignore
                message=f'Invalid response content. {str(ke)} in the response.',
                errors=[],
            )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Dataset:
        for required_field in [
            'id',
            'name',
            'version',
            'info',
            'file_list',
            'organization_name',
            'project_name',
        ]:
            if required_field not in data:
                raise KeyError("Required {required_field} in not found")
        # v2 version of DatasetInfo required only columns
        # core_objects.DatasetInfo requires display_name
        # Hence to keep python-client backward compatible with fiddler-server, name is added.
        datasetinfo_json = data['info']
        if 'name' not in datasetinfo_json:
            datasetinfo_json['name'] = data['name']
        return cls(
            id=data['id'],
            name=data['name'],
            version=data['version'],
            info=DatasetInfo.from_dict(datasetinfo_json),
            file_list=data['file_list'],
            organization_name=data['organization_name'],
            project_name=data['project_name'],
        )


class DatasetIngest:
    def __init__(
        self,
        name: str,
        file_name: List[str],
        info: Optional[DatasetInfo] = None,
        file_type: Optional[FileType] = None,
        file_schema: Optional[dict] = None,
        upload_type: UploadType = UploadType.DATASET,
    ) -> None:
        self.name = name
        self.file_name = file_name
        self.info = info
        self.file_type = file_type
        self.file_schema = file_schema
        self.upload_type = upload_type

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {
            'name': self.name,
            'file_name': self.file_name,
            'upload_type': self.upload_type.name,
        }
        if self.info:
            res['info'] = self.info.to_dict()
        if self.file_type:
            res['file_type'] = self.file_type
        if self.file_schema:
            res['file_schema'] = self.file_schema
        return res
