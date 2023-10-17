from collections import namedtuple
from functools import wraps
from http import HTTPStatus
from typing import List, NamedTuple

try:
    from simplejson import JSONDecodeError
except ImportError:
    from json import JSONDecodeError

from requests.exceptions import HTTPError

from fiddler.utils import logging

logger = logging.getLogger(__name__)


class NotSupported(Exception):
    pass


class AsyncJobFailed(Exception):
    pass


class ErrorResponseHandler:
    def __init__(self, http_error: HTTPError) -> None:
        self.http_error = http_error
        self.response = http_error.response
        self.ErrorResponse = namedtuple(
            'ErrorResponse', ['status_code', 'error_code', 'message', 'errors']
        )

    def get_error_details(self) -> NamedTuple:
        status_code = self.response.status_code
        try:
            error_details = self.response.json().get('error', {})
        except JSONDecodeError:
            raise FiddlerAPIException(
                status_code=self.response.status_code,
                error_code=self.response.status_code,
                message=f'Invalid response content-type. {self.response.status_code}:{self.response.content}',
                errors=[],
            )
        error_code = error_details.get('code')
        message = error_details.get('message')
        errors = error_details.get('errors')
        return self.ErrorResponse(status_code, error_code, message, errors)


class BaseException(Exception):
    pass


class FiddlerException(BaseException):
    '''
    Exception class to handle non API response exceptions
    '''


class FiddlerAPIException(BaseException):
    '''
    Exception class to specifically handle Fiddler's API error responses structure.
    This is a generic API response exception class
    '''

    # @TODO: Handle standard API error response.
    # How to surface error messages coming form the server. Server responds error messages in a list. Which error to surface?
    def __init__(
        self, status_code: int, error_code: int, message: str, errors: List[str]
    ) -> None:
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.errors = errors
        super().__init__(self.message)


class FiddlerAPIBadRequestException(FiddlerAPIException):
    pass


class FiddlerAPINotFoundException(FiddlerAPIException):
    pass


class FiddlerAPIConflictException(FiddlerAPIException):
    pass


class FiddlerAPIForbiddenException(FiddlerAPIException):
    pass


class FiddlerAPIInternalServerErrorException(FiddlerAPIException):
    pass


map_except_resp_code = {
    HTTPStatus.BAD_REQUEST: FiddlerAPIBadRequestException,  # 400
    HTTPStatus.FORBIDDEN: FiddlerAPIForbiddenException,  # 403
    HTTPStatus.NOT_FOUND: FiddlerAPINotFoundException,  # 404
    HTTPStatus.CONFLICT: FiddlerAPIConflictException,  # 409
    HTTPStatus.INTERNAL_SERVER_ERROR: FiddlerAPIInternalServerErrorException,  # 500
}


def handle_api_error_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPError as error:
            logger.error(
                'HTTP request to %s failed with %s - %s',
                getattr(error.request, 'url', 'unknown'),
                getattr(error.response, 'status_code', 'unknown'),
                getattr(error.response, 'content', 'missing'),
            )
            error_response = ErrorResponseHandler(error).get_error_details()
            # raise status_code specific exceptions else raise generic FiddlerAPIException
            exec_class = map_except_resp_code.get(
                error_response.status_code, FiddlerAPIException
            )
            raise exec_class(
                error_response.status_code,
                error_response.error_code,
                error_response.message,
                error_response.errors,
            ) from None
            # disabling automatic exception chaining
            # ref: https://docs.python.org/3/tutorial/errors.html#exception-chaining

    return wrapper
