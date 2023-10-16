import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import parse_obj_as

from fiddler.api.model_artifact_deploy import (
    ModelArtifactDeployer,
    MultiPartModelArtifactDeployer,
)
from fiddler.constants import MULTI_PART_CHUNK_SIZE
from fiddler.core_objects import ModelInfo
from fiddler.libs.http_client import RequestClient
from fiddler.schema.model import Model
from fiddler.schema.model_deployment import ArtifactType, DeploymentParams
from fiddler.utils.decorators import check_version, handle_api_error_response
from fiddler.utils.helpers import get_model_artifact_info, read_model_yaml
from fiddler.utils.logger import get_logger
from fiddler.utils.response_handler import APIResponseHandler, PaginatedResponseHandler
from fiddler.utils.validations import validate_artifact_dir

logger = get_logger(__name__)


class ModelMixin:
    client: RequestClient
    organization_name: str

    @handle_api_error_response
    def get_models(self, project_id: str) -> List[Model]:
        """
        Get list of all models belonging to a project

        :params project_id: The project for which you want to get the models
        :returns: List containing Model objects
        """
        response = self.client.get(
            url='models',
            params={
                'organization_name': self.organization_name,
                'project_name': project_id,
            },
        )
        items = PaginatedResponseHandler(response).get_pagination_items()
        return parse_obj_as(List[Model], items)

    @handle_api_error_response
    def get_model_names(self, project_id: str) -> List[str]:
        """
        List the ids of all models in the project.

        :param project_id: The unique identifier of the project on Fiddler
        :returns: List of strings containing the ids of each model.
        """
        models = self.get_models(project_id=project_id)
        return [m.name for m in models]

    @handle_api_error_response
    def get_model(self, project_id: str, model_id: str) -> Model:
        """
        Get the details of a model.

        :params project_id: The project to which the model belongs to
        :params model_id: The model name of which you need the details
        :returns: Model object which contains the details
        """
        response = self.client.get(
            url=f'models/{self.organization_name}:{project_id}:{model_id}',
        )
        response_handler = APIResponseHandler(response)
        return Model.deserialize(response_handler)

    def list_models(self, project_id: str) -> List[str]:
        """
        List the ids of all models in the project.

        :param project_id: The unique identifier of the project on Fiddler
        :returns: List of strings containing the ids of each model.
        """

        return self.get_model_names(project_id=project_id)

    def get_model_info(
        self,
        project_id: str,
        model_id: str,
    ) -> ModelInfo:
        """Get ModelInfo for a model.

        :params project_id: The project to which the model belongs to
        :params model_id: The model name of which you need the details

        :returns: A fiddler.ModelInfo object describing the model.
        """

        model_info_dict = self.get_model(project_id=project_id, model_id=model_id).info
        return ModelInfo.from_dict(model_info_dict)

    @handle_api_error_response
    def add_model(  # noqa: C901
        self,
        project_id: str,
        model_id: str,
        dataset_id: str,
        model_info: ModelInfo,
        is_sync: bool = True,
    ) -> Model:
        """
        Onboard model to Fiddler Platform
        :params project_id: The project to which the model belongs to
        :params model_id: The model name of which you need the details
        :param dataset_id: name of the dataset
        :param is_sync: Wait for job to complete or return after submitting
        :param model_info: (Deprecated) model related information from user
        """

        if not model_info:
            raise ValueError('Please pass a valid ModelInfo object')

        model_info.datasets = [dataset_id]

        request_body = {
            'name': model_id,
            'project_name': project_id,
            'organization_name': self.organization_name,
            'info': model_info.to_dict(),
        }

        response = self.client.post(
            url='models',
            data=request_body,
        )

        logger.info('Model %s added to %s project', model_id, project_id)

        model = Model.deserialize(APIResponseHandler(response))
        if model.job_uuid and is_sync:
            job_name = f'Model[{project_id}/{model_id}] - Initializing monitoring'
            self.wait_for_job(uuid=model.job_uuid, job_name=job_name)  # type: ignore  # noqa

        return model

    @handle_api_error_response
    def update_model(
        self,
        model_id: str,
        project_id: str,
        info: Optional[ModelInfo] = None,
        file_list: Optional[List[Dict[str, Any]]] = None,
        framework: Optional[str] = None,
        requirements: Optional[str] = None,
    ) -> Model:
        """
        Update model metadata like model info, file

        :param project_id: project name where the model will be added
        :type project_id: string
        :param model_id: name of the model
        :type model_id: string
        :param info: model related information passed as dictionary from user
        :type info: ModelInfo object
        :param file_list: Artifact file list
        :type info: List of dictionaries
        :param framework: Model framework name
        :type framework: string
        :param requirements: Requirements
        :type requirements: string
        :return: Model object which contains the model details
        """
        body: Dict[str, Any] = {}

        if info:
            body['info'] = info.to_dict()

        if file_list:
            body['file_list'] = file_list

        if framework:
            body['framework'] = framework

        if requirements:
            body['requirements'] = requirements

        response = self.client.patch(
            url=f'models/{self.organization_name}:{project_id}:{model_id}',
            data=body,
        )
        logger.info('Model[%s/%s] - Updated model', project_id, model_id)

        return Model.deserialize(APIResponseHandler(response))

    @handle_api_error_response
    def delete_model(
        self,
        project_id: str,
        model_id: str,
    ) -> None:
        """
        Delete a model

        :params model_id: Model name to be deleted
        :params project_id: Project name to which the model belongs to.

        :returns: None
        """

        logger.info('Deleting model %s from %s project', model_id, project_id)
        self.client.delete(
            url=f'models/{self.organization_name}:{project_id}:{model_id}',
        )
        logger.info('Deleted model %s from %s project', model_id, project_id)

    @handle_api_error_response
    def add_model_surrogate(
        self,
        project_id: str,
        model_id: str,
        deployment_params: Optional[DeploymentParams] = None,
        wait: bool = True,
    ) -> str:
        """
        Add surrogate model to an existing model

        :params project_id: Project name to which the model belongs to.
        :params model_id: Model name to be added
        :param deployment_params: Model deployment parameters
        :param wait: Whether to wait for job to complete or return after submitting
            the job
        :return: Async job uuid
        """

        return self._deploy_surrogate_model(
            model_name=model_id,
            project_name=project_id,
            deployment_params=deployment_params,
            wait=wait,
            update=False,
        )

    @check_version(version_expr='>=23.1.0')
    @handle_api_error_response
    def update_model_surrogate(
        self,
        project_id: str,
        model_id: str,
        deployment_params: Optional[DeploymentParams] = None,
        is_sync: bool = True,
    ) -> str:
        """
        Re-generate surrogate model

        :params project_id: Project name to which the model belongs to.
        :params model_id: Model name to be updated
        :param is_sync: Whether to wait for job to complete or return after submitting
            the job
        :param deployment_params: Model deployment parameters

        :return: Async job uuid
        """

        return self._deploy_surrogate_model(
            model_name=model_id,
            project_name=project_id,
            deployment_params=deployment_params,
            wait=is_sync,
            update=True,
        )

    def _deploy_surrogate_model(
        self,
        model_name: str,
        project_name: str,
        deployment_params: Optional[DeploymentParams] = None,
        wait: bool = True,
        update: bool = False,
    ) -> str:
        """
        Add surrogate model to an existing model
        :param model_name: Model name
        :param project_name: Project name
        :param deployment_params: Model deployment parameters
        :param wait: Whether to wait for job to complete or return after submitting
            the job
        :param update: Set True for re-generating surrogate model, otherwise False
        :return: Async job uuid
        """
        payload: Dict[str, Any] = {
            'model_name': model_name,
            'project_name': project_name,
            'organization_name': self.organization_name,
        }

        if deployment_params:
            deployment_params.artifact_type = ArtifactType.SURROGATE
            payload['deployment_params'] = deployment_params.dict(exclude_unset=True)

        model_name = f'{self.organization_name}:{project_name}:{model_name}'
        url = f'models/{model_name}/deploy-surrogate'
        method: Any = self.client.put if update else self.client.post
        response = method(url=url, data=payload)

        data = APIResponseHandler(response).get_data()
        job_uuid = data['job_uuid']

        logger.info(
            'Model[%s/%s] - Submitted job (%s) for deploying a surrogate model',
            project_name,
            model_name,
            job_uuid,
        )

        if wait:
            job_name = f'Model[{project_name}/{model_name}] - Deploy a surrogate model'
            self.wait_for_job(uuid=job_uuid, job_name=job_name)  # type: ignore  # noqa

        return job_uuid

    def _deploy_model_artifact(
        self,
        project_name: str,
        model_name: str,
        artifact_dir: Union[str, Path],
        deployment_params: Optional[DeploymentParams] = None,
        wait: bool = True,
        update: bool = False,
    ) -> str:
        """
        Upload and deploy model artifact for an existing model
        :param model_name: Model name
        :param project_name: Project name
        :param artifact_dir: Model artifact directory
        :param deployment_params: Model deployment parameters
        :param wait: Whether to wait for async job to finish or return
        :param update: Set True for updating artifact, False for adding artifact
        :return: Async job uuid
        """
        artifact_dir = (
            Path(artifact_dir) if isinstance(artifact_dir, str) else artifact_dir
        )
        validate_artifact_dir(artifact_dir)

        if (
            deployment_params
            and deployment_params.artifact_type == ArtifactType.SURROGATE
        ):
            raise ValueError(
                f'{ArtifactType.SURROGATE} artifact_type is an invalid value for this '
                f'method. Use {ArtifactType.PYTHON_PACKAGE} instead.'
            )

        self._update_model_on_artifact_upload(
            model_name=model_name, project_name=project_name, artifact_dir=artifact_dir
        )

        with tempfile.TemporaryDirectory() as tmp:
            # Archive model artifact directory
            logger.info(
                'Model[%s/%s] - Tarring model artifact directory - %s',
                project_name,
                model_name,
                artifact_dir,
            )
            file_path = shutil.make_archive(
                base_name=str(Path(tmp) / 'files'),
                format='tar',
                root_dir=str(artifact_dir),
                base_dir='.',
            )

            logger.info(
                'Model[%s/%s] - Model artifact tar file created at %s',
                project_name,
                model_name,
                file_path,
            )

            deployer_class: Any = None
            # Choose deployer based on archive file size
            if os.path.getsize(file_path) < MULTI_PART_CHUNK_SIZE:
                deployer_class = ModelArtifactDeployer
            else:
                deployer_class = MultiPartModelArtifactDeployer

            deployer = deployer_class(
                client=self.client,
                model_name=model_name,
                project_name=project_name,
                organization_name=self.organization_name,
                update=update,
            )

            job_uuid = deployer.deploy(
                file_path=Path(file_path), deployment_params=deployment_params
            )

        logger.info(
            'Model[%s/%s] - Submitted job (%s) for deploying model artifact',
            project_name,
            model_name,
            job_uuid,
        )

        if wait:
            job_name = f'Model[{project_name}/{model_name}] - Deploy model artifact'
            self.wait_for_job(uuid=job_uuid, job_name=job_name)  # type: ignore # noqa

        return job_uuid

    @handle_api_error_response
    def add_model_artifact(
        self,
        project_id: str,
        model_id: str,
        model_dir: str,
        deployment_params: Optional[DeploymentParams] = None,
        wait: bool = True,
    ) -> str:
        """
        Add model artifact to an existing model

        :params project_id: Project name to which the model belongs to.
        :params model_id: Model name to be added
        :param model_dir: Model artifact directory
        :param deployment_params: Model deployment parameters
        :param wait: Whether to wait for async job to finish or return
        :return: Async job uuid
        """

        return self._deploy_model_artifact(
            project_name=project_id,
            model_name=model_id,
            artifact_dir=model_dir,
            deployment_params=deployment_params,
            wait=wait,
            update=False,
        )

    @check_version(version_expr='>=22.12.0')
    @handle_api_error_response
    def update_model_artifact(
        self,
        project_id: str,
        model_id: str,
        model_dir: str,
        deployment_params: Optional[DeploymentParams] = None,
        wait: bool = True,
    ) -> str:
        """
        Update model artifact of an existing model

        :params project_id: Project name to which the model belongs to.
        :params model_id: Model name to be added
        :param model_dir: Model artifact directory
        :param deployment_params: Model deployment parameters
        :param wait: Whether to wait for async job to finish or return
        :return: Async job uuid
        """

        return self._deploy_model_artifact(
            project_name=project_id,
            model_name=model_id,
            artifact_dir=model_dir,
            deployment_params=deployment_params,
            wait=wait,
            update=True,
        )

    def _update_model_on_artifact_upload(
        self, model_name: str, project_name: str, artifact_dir: Path
    ) -> None:
        """Update model metadata based on artifact dir contents"""
        file_list = get_model_artifact_info(artifact_dir=artifact_dir)
        model_info = read_model_yaml(artifact_dir=artifact_dir)

        self.update_model(
            model_id=model_name,
            project_id=project_name,
            info=model_info,
            file_list=file_list,
        )

    @handle_api_error_response
    def download_artifacts(
        self, project_id: str, model_id: str, output_dir: Path
    ) -> None:
        """
        download the model binary, package.py and model.yaml to the given
        output dir.

        :param project_id: Project name
        :param model_id: Model name
        :param output_dir: output directory
        :return: None
        """

        if output_dir.exists():
            raise ValueError(f'output dir already exists {output_dir}')

        model_id = f'{self.organization_name}:{project_id}:{model_id}'
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Download tar file
            tar_file_path = os.path.join(tmp_dir, 'artifact.tar')

            with self.client.get(url=f'models/{model_id}/download-artifacts') as r:
                r.raise_for_status()
                with open(tar_file_path, mode='wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            os.makedirs(output_dir, exist_ok=True)
            shutil.unpack_archive(tar_file_path, extract_dir=output_dir, format='tar')
