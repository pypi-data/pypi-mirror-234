from typing import Any, Dict, Optional

from fiddler.libs.http_client import RequestClient
from fiddler.schema.model_deployment import ModelDeployment
from fiddler.utils.decorators import check_version, handle_api_error_response
from fiddler.utils.logger import get_logger

logger = get_logger(__name__)


class ModelDeploymentMixin:
    """Model deployment api handler"""

    client: RequestClient
    organization_name: str

    @check_version(version_expr='>=23.1.0')
    @handle_api_error_response
    def get_model_deployment(
        self,
        project_id: str,
        model_id: str,
    ) -> ModelDeployment:
        """
        Get model deployment object
        :params project_id: Project name
        :params model_id: Model name
        :return: Model deployment object
        """

        model_id_url = f'{self.organization_name}:{project_id}:{model_id}'
        response = self.client.get(url=f'model-deployments/{model_id_url}')

        return ModelDeployment(**response.json().get('data'))

    @check_version(version_expr='>=23.1.0')
    @handle_api_error_response
    def update_model_deployment(
        self,
        project_id: str,
        model_id: str,
        active: Optional[bool] = None,
        replicas: Optional[int] = None,
        cpu: Optional[int] = None,
        memory: Optional[int] = None,
        wait: bool = True,
    ) -> ModelDeployment:
        """
        Update model deployment fields like replicas, cpu, memory

        :param project_id: Project name
        :param model_id: Model name
        :param active: Set False to scale down model deployment and True to scale up
        :param replicas: Number of model deployment replicas to run
        :param cpu: Amount of milli cpus to allocate for each replica
        :param memory: Amount of mebibytes memory to allocate for each replica
        :param wait: Whether to wait for async job to finish or return
        :return: Model deployment object
        """

        body: Dict[str, Any] = {}

        if active is not None:
            body['active'] = active

        if replicas is not None:
            body['replicas'] = replicas

        if cpu is not None:
            body['cpu'] = cpu

        if memory is not None:
            body['memory'] = memory

        if not body:
            raise ValueError('Pass at least one parameter to update model deployment')

        model_id = f'{self.organization_name}:{project_id}:{model_id}'
        response = self.client.patch(
            url=f'model-deployments/{model_id}',
            data=body,
        )

        model_deployment = ModelDeployment(**response.json().get('data'))

        logger.info(
            'Model[%s/%s] - Submitted job (%s) for updating model deployment',
            project_id,
            model_id,
            model_deployment.job_uuid,
        )

        if wait:
            job_name = f'Model[{project_id}/{model_id}] - Update model deployment'
            self.wait_for_job(uuid=model_deployment.job_uuid, job_name=job_name)  # type: ignore # noqa

        return model_deployment
