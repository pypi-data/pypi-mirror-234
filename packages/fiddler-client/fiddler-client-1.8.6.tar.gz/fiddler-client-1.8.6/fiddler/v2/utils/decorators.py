from functools import wraps
from typing import Any, Callable

from ..utils.exceptions import NotSupported
from ..utils.helpers import match_semvar


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

    def decorator(func) -> Callable:
        @wraps(func)
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            if not match_semvar(self.server_info.server_version, version_expr):
                raise NotSupported(
                    f'{func.__name__} method is supported with server version '
                    f'{version_expr}, but the current server version is '
                    f'{self.server_info.server_version}'
                )

            return func(self, *args, **kwargs)

        return wrapper

    return decorator
