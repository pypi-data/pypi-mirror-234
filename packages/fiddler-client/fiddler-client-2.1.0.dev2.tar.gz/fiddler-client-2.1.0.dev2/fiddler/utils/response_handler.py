from typing import Any, Dict, List

try:
    from simplejson import JSONDecodeError
except ImportError:
    from json import JSONDecodeError  # type: ignore

import requests

from fiddler.exceptions import HttpException
from fiddler.utils.logger import get_logger

logger = get_logger(__name__)


class BaseResponseHandler:
    def __init__(self, response: requests.Response) -> None:
        self.response = response
        logger.debug(self.response.content)

    def get_data(self) -> Dict[str, Any]:
        try:
            dict_response = self.response.json().get('data')
        except JSONDecodeError:
            raise HttpException(
                status_code=self.response.status_code,
                error_code=self.response.status_code,
                message=f'Invalid response content-type. '
                f'{self.response.status_code}:{self.response.content.decode("utf-8")}',
                errors=[],
            )
        return dict_response

    def get_status_code(self) -> int:
        return self.response.status_code


class PaginatedResponseHandler(BaseResponseHandler):
    '''
    Handle fiddler OAS's standard Paginated response
    '''

    def get_pagination_items(self) -> List[dict]:
        return self.get_data().get('items', [])


class APIResponseHandler(BaseResponseHandler):
    '''
    Handle fiddler OAS's standard API Response
    '''


class JobResponseHandler(BaseResponseHandler):
    def __init__(self, response: requests.Response) -> None:
        super().__init__(response)
        data = self.get_data()
        self.uuid = data.get('uuid')
        self.name = data.get('name')
        self.status = data.get('status')
        self.progress = data.get('progress')
        self.error_message = data.get('error_message')
        self.error_reason = data.get('error_reason')
        self.extras = data.get('extras')
