import time
from urllib.parse import urljoin

import requests
from requests import Response, HTTPError

from biolib.biolib_logging import logger_no_user_data
from biolib.typing_utils import Dict, Optional, Union
from biolib.biolib_api_client import BiolibApiClient as DeprecatedApiClient

OptionalHeaders = Optional[Dict[str, Union[str, None]]]


class ApiClient:

    def __init__(self):
        self._session = requests.session()

    def get(
            self,
            url: str,
            params: Optional[Dict[str, Union[str, int]]] = None,
            headers: OptionalHeaders = None,
            authenticate: bool = True,
    ) -> Response:
        retries = 10
        for retry_count in range(retries):
            if retry_count > 0:
                time.sleep(5 * retry_count)
                logger_no_user_data.debug('Retrying HTTP GET request...')
            try:
                response: Response = self._session.get(
                    headers=self._get_headers(headers, authenticate),
                    params=params,
                    timeout=60,
                    url=self._get_absolute_url(url),
                )
                if response.status_code == 502:
                    logger_no_user_data.debug(f'HTTP GET request failed with status 502 for "{url}"')
                    continue

                ApiClient.raise_for_status(response)
                return response
            except requests.exceptions.ReadTimeout:
                logger_no_user_data.debug(f'HTTP GET request failed with read timeout for "{url}"')
                continue

        raise Exception(f'HTTP GET request failed after {retries} retries for "{url}"')

    def post(self, path: str, data: Union[Dict, bytes], headers: OptionalHeaders = None) -> Response:
        retries = 3
        for retry_count in range(retries):
            if retry_count > 0:
                time.sleep(5 * retry_count)
                logger_no_user_data.debug('Retrying HTTP POST request...')
            try:
                response: Response = self._session.post(
                    headers=self._get_headers(headers),
                    data=data if not isinstance(data, dict) else None,
                    json=data if isinstance(data, dict) else None,
                    timeout=10 if isinstance(data, dict) else 180,  # TODO: Calculate timeout based on data size
                    url=self._get_absolute_url(path),
                )
                if response.status_code == 502:
                    logger_no_user_data.debug(f'HTTP POST request failed with status 502 for "{path}"')
                    continue

                ApiClient.raise_for_status(response)
                return response
            except requests.exceptions.ReadTimeout:
                logger_no_user_data.debug(f'HTTP POST request failed with read timeout for "{path}"')
                continue

        raise Exception(f'HTTP POST request failed after {retries} retries for "{path}"')

    def patch(self, path: str, data: Dict, headers: OptionalHeaders = None) -> Response:
        response: Response = self._session.patch(
            headers=self._get_headers(headers),
            json=data,
            timeout=10,
            url=self._get_absolute_url(path),
        )
        ApiClient.raise_for_status(response)
        return response

    @staticmethod
    def raise_for_status(response):
        # Logic taken from `requests.Response.raise_for_status()`
        http_error_msg = ''
        reason = response.text
        if 400 <= response.status_code < 500:
            http_error_msg = u'%s Client Error: %s for url: %s' % (response.status_code, reason, response.url)

        elif 500 <= response.status_code < 600:
            http_error_msg = u'%s Server Error: %s for url: %s' % (response.status_code, reason, response.url)

        if http_error_msg:
            raise HTTPError(http_error_msg, response=response)

    @staticmethod
    def _get_headers(opt_headers: OptionalHeaders = None, authenticate: bool = True) -> Dict[str, str]:
        # Only keep header keys with a value
        headers: Dict[str, str] = {key: value for key, value in (opt_headers or {}).items() if value}

        deprecated_api_client = DeprecatedApiClient.get()

        if deprecated_api_client.is_signed_in:
            deprecated_api_client.refresh_access_token()

        # Adding access_token outside is_signed_in check as job_worker.py currently sets access_token
        # without setting refresh_token
        access_token = deprecated_api_client.access_token
        if access_token and authenticate:
            headers['Authorization'] = f'Bearer {access_token}'

        return headers

    @staticmethod
    def _get_absolute_url(path: str) -> str:
        deprecated_api_client = DeprecatedApiClient.get()
        base_api_url = urljoin(deprecated_api_client.base_url, '/api/')
        return urljoin(base_api_url, path.strip('/') + '/')
