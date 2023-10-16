from collections import namedtuple
from typing import List, NamedTuple

try:
    from simplejson import JSONDecodeError
except ImportError:
    from json import JSONDecodeError  # type: ignore

from requests.exceptions import HTTPError
from fiddler.utils.logger import get_logger

logger = get_logger(__name__)


class NotSupported(Exception):
    pass


class AsyncJobFailed(Exception):
    pass


class ErrorResponseHandler:
    def __init__(self, http_error: HTTPError) -> None:
        self.http_error = http_error
        self.response = http_error.response
        self.ErrorResponse = namedtuple(  # type: ignore
            'ErrorResponse', ['status_code', 'error_code', 'message', 'errors']
        )

    def get_error_details(self) -> NamedTuple:
        status_code = self.response.status_code
        try:
            error_details = self.response.json().get('error', {})
        except JSONDecodeError:
            raise HttpException(
                status_code=self.response.status_code,
                error_code=self.response.status_code,
                message=f'Invalid response content-type. '
                f'{self.response.status_code}:{self.response.content}',
                errors=[],
            )
        error_code = error_details.get('code')
        message = error_details.get('message')
        errors = error_details.get('errors')
        return self.ErrorResponse(status_code, error_code, message, errors)  # type: ignore


class FiddlerBaseException(Exception):
    pass


class ApiException(FiddlerBaseException):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class HttpException(FiddlerBaseException):
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


class BadRequest(HttpException):
    pass


class NotFound(HttpException):
    pass


class Conflict(HttpException):
    pass


class Forbidden(HttpException):
    pass


class InternalServerError(HttpException):
    pass
