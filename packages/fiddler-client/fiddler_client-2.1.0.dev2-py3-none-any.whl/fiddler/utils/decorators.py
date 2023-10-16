import warnings
from functools import wraps
from http import HTTPStatus
from typing import no_type_check, Any, Callable

from requests.exceptions import HTTPError

from fiddler.constants import COMPAT_MAPPING
from fiddler.exceptions import (
    NotSupported,
    ErrorResponseHandler,
    HttpException,
    BadRequest,
    Forbidden,
    Conflict,
    NotFound,
    InternalServerError,
)
from fiddler.utils.helpers import match_semver
from fiddler.utils.logger import get_logger

logger = get_logger(__name__)

map_except_resp_code = {
    HTTPStatus.BAD_REQUEST: BadRequest,  # 400
    HTTPStatus.FORBIDDEN: Forbidden,  # 403
    HTTPStatus.NOT_FOUND: NotFound,  # 404
    HTTPStatus.CONFLICT: Conflict,  # 409
    HTTPStatus.INTERNAL_SERVER_ERROR: InternalServerError,  # 500
}


def check_version(version_expr: str) -> Callable:
    """
    Check version_expr against server version before making an API call

    Usage:
        @check_version(version_expr=">=23.1.0")
        @handle_api_error_response
        def get_model_deployment(...):
            ...

    Add this decorator on top of other decorators to make sure version check happens
    before doing any other work.

    :param version_expr: Supported version to match with. Read more at VersionInfo.match
    :return: Decorator function
    """

    @no_type_check
    def decorator(func) -> Callable:
        @wraps(func)
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            if not match_semver(self.server_info.server_version, version_expr):
                raise NotSupported(
                    f'{func.__name__} method is supported with server version '
                    f'{version_expr}, but the current server version is '
                    f'{self.server_info.server_version}'
                )

            return func(self, *args, **kwargs)

        return wrapper

    return decorator


@no_type_check
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
            # raise status_code specific exceptions else raise generic HttpException
            exec_class = map_except_resp_code.get(
                error_response.status_code, HttpException
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


@no_type_check
def compat_warning(func):
    '''Compatibilty warnings'''

    @wraps(func)
    def wrapper(*args, **kwargs):
        old_params = COMPAT_MAPPING.keys()
        accepted_kwargs = [param for param in kwargs.keys() if param in old_params]
        compat_params = ', '.join(accepted_kwargs)
        new_params = ', '.join([COMPAT_MAPPING[key] for key in accepted_kwargs])

        warnings.warn(
            f'WARNING: {compat_params} is/are deprecated and will be removed from '
            f'future versions. Use {new_params} instead',
            FutureWarning,
        )
        return func(*args, **kwargs)

    return wrapper
