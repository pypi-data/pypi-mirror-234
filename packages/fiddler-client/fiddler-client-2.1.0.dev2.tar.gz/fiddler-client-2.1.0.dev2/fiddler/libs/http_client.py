from copy import deepcopy
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests
import simplejson
from requests.adapters import HTTPAdapter
from requests_toolbelt.multipart.encoder import MultipartEncoder

from fiddler.exceptions import ApiException
from fiddler.utils.logger import get_logger

APP_JSON_CONTENT_TYPE = 'application/json'


logger = get_logger(__name__)


class RequestClient:
    def __init__(
        self, base_url: str, headers: Dict[str, str], verify: bool = True
    ) -> None:
        self.base_url = base_url
        self.headers = headers
        self.headers.update({'Content-Type': APP_JSON_CONTENT_TYPE})
        self.session = requests.Session()
        self.session.verify = verify
        adapter = HTTPAdapter(
            pool_connections=25,
            pool_maxsize=25,
        )
        self.session.mount(self.base_url, adapter)

    def call(
        self,
        *,
        method: str,
        url: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
        timeout: Optional[int] = None,
        files_encoders: Optional[Dict[str, MultipartEncoder]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        """
        Make request to server

        :param files_encoders  (optional) Dictionary of 'filename': file-like-objects
            for multipart encoding upload. Make sure all MultipartEncoder values have
            same content_type.
        """

        full_url = urljoin(self.base_url + '/', url)

        request_headers = self.headers
        # override/update headers coming from the calling method
        if headers:
            request_headers = deepcopy(self.headers)
            request_headers.update(headers)

        content_type = request_headers.get('Content-Type')
        if data and content_type == APP_JSON_CONTENT_TYPE:
            data = simplejson.dumps(data, ignore_nan=True)  # type: ignore

        kwargs.setdefault('allow_redirects', True)
        # requests is not able to pass the value of self.session.verify to the
        # verify param in kwargs when REQUESTS_CA_BUNDLE is set.
        # So setting that as default here
        kwargs.setdefault('verify', self.session.verify)
        try:
            if files_encoders:
                encoders = list(files_encoders.values())
                if encoders:
                    request_headers['Content-Type'] = encoders[0].content_type
                response = self.session.request(
                    method,
                    full_url,
                    params=params,
                    files=files_encoders,
                    headers=request_headers,
                    timeout=timeout,
                    **kwargs,
                )
            else:
                response = self.session.request(
                    method,
                    full_url,
                    params=params,
                    data=data,
                    headers=request_headers,
                    timeout=timeout,
                    **kwargs,
                )
        except requests.exceptions.Timeout:
            logger.error(f'{method} call failed with Timeout error for URL {url}')
            message = f'Request timed out while trying to reach endpoint {url}'
            raise ApiException(message=message)
        except requests.exceptions.ConnectionError:
            logger.error(f'{method} call failed with ConnectionError for URL {url}')
            message = f'Unable to reach endpoint {url}'
            raise ApiException(message=message)
        except requests.exceptions.RequestException:
            # catastrophic error.
            logger.error(f'{method} call failed with RequestException for URL {url}')
            message = f'Failed to reach endpoint {url}'
            raise ApiException(message=message)

        response.raise_for_status()
        return response

    def get(
        self,
        *,
        url: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        timeout: Optional[int] = None,
        **kwargs: Dict[str, Any],
    ) -> requests.Response:
        logger.info(f'Making GET call for {url}')
        return self.call(
            method='GET',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def delete(
        self,
        *,
        url: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        timeout: Optional[int] = None,
        **kwargs: Dict[str, Any],
    ) -> requests.Response:
        logger.info(f'Making DELETE call for {url}')
        return self.call(
            method='DELETE',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def post(
        self,
        *,
        url: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        timeout: Optional[int] = None,
        data: Optional[dict] = None,
        files_encoders: Optional[Dict[str, MultipartEncoder]] = None,
        **kwargs: Dict[str, Any],
    ) -> requests.Response:
        logger.info(f'Making POST call for {url}')
        return self.call(
            method='POST',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            files_encoders=files_encoders,
            **kwargs,
        )

    def put(
        self,
        *,
        url: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        timeout: Optional[int] = None,
        data: Optional[dict] = None,
        **kwargs: Dict[str, Any],
    ) -> requests.Response:
        logger.info(f'Making PUT call for {url}')
        return self.call(
            method='PUT',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            **kwargs,
        )

    def patch(
        self,
        *,
        url: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        timeout: Optional[int] = None,
        data: Optional[dict] = None,
        **kwargs: Dict[str, Any],
    ) -> requests.Response:
        logger.info(f'Making PATCH call for {url}')
        return self.call(
            method='PATCH',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            **kwargs,
        )
