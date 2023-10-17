"""
A collection of functions for integrating with the Archimedes API
"""
# pylint: disable=no-member

from http import HTTPStatus

import orjson
import requests
from requests.exceptions import (  # pylint:disable=redefined-builtin
    ConnectionError,
    ConnectTimeout,
    HTTPError,
    JSONDecodeError,
    Timeout,
)
from retrying import retry

from archimedes import NoneAuth, get_auth
from archimedes.configuration import get_api_timeout, get_archimedes_user_agent
from archimedes.logger import logger

RETRY_EXCEPTIONS = (ConnectionError, ConnectTimeout, HTTPError, Timeout)


class ArchimedesApi:  # pylint:disable=too-few-public-methods
    """
    Make request to the Archimedes API
    """

    def __init__(self):
        self.session = requests.Session()

    def request(  # pylint:disable=too-many-arguments,too-many-locals
        self,
        url,
        method="GET",
        access_token=None,
        retry_count=2,
        retry_delay=2,
        **kwargs,
    ):
        """
        Make request to the Archimedes API. It automatically retries retry_count times
        on failure.

        Args:
            url:
                full URL of the API endpoint.
            method:
                HTTP method to use.
            access_token:
                authorization token; if None, tries to get the token automatically based
                on the authentication configuration.
            retry_count:
                number of times to retry the request. if 0, only one request is made.
            retry_delay:
                delay between retries in seconds.
            **kwargs:
                other kwargs to requests.request.

        Returns:
            Response from the API as a python object.
        """
        logger.debug("Making Archimedes API %s request to %s: %s", method, url, kwargs)
        if access_token is None:
            archimedes_auth = get_auth()
            if archimedes_auth is None:
                raise NoneAuth(
                    "access_token parameter must be passed when using "
                    "USE_WEB_AUTHENTICATION"
                )
            access_token = archimedes_auth.get_access_token_silent()

        timeout = kwargs.pop("timeout", get_api_timeout())

        headers = kwargs.pop("headers", {})
        headers.update({"Authorization": f"Bearer {access_token}"})

        user_agent = get_archimedes_user_agent()
        if user_agent is not None:
            headers.update({"User-Agent": user_agent})

        # remove param keys if values are empty
        params = kwargs.get("params", None)
        if params:
            params = {k: v for k, v in params.items() if v is not None}
            kwargs["params"] = params

        @retry(
            stop_max_attempt_number=retry_count + 1,
            wait_fixed=retry_delay * 1000,
            retry_on_exception=RETRY_EXCEPTIONS,
        )
        def _make_request():
            return self.session.request(
                method, url, headers=headers, timeout=timeout, **kwargs
            )

        response = _make_request()

        if response.status_code not in [HTTPStatus.OK, HTTPStatus.CREATED]:
            try:
                response_json = response.json()
                if "message" in response_json:
                    error_message = response_json.get("message")
                elif "detail" in response_json:
                    error_message = response_json.get("detail")
                else:
                    error_message = response.text
            except JSONDecodeError:
                error_message = response.content
            params_str = str(kwargs.get("params"))
            data_str = str(kwargs.get("data"))
            raise HTTPError(
                f"API Error with status code {response.status_code} while requesting {url} with parameters "
                f"{params_str} and data {data_str}: {error_message}"
            )

        logger.debug(
            "Response from Archimedes for API (url: %s, kwargs: %s): %s",
            url,
            kwargs,
            response.text[:250],
        )
        return orjson.loads(response.text)


api = ArchimedesApi()
