from typing import Any, Callable, TypeVar

import requests
from requests import Response
from returns.result import Failure, Result, Success
import seaplane_framework.api
from seaplane_framework.api import ApiClient

from ..configuration import Configuration, config
from ..logging import log
from ..model.errors import HTTPError
from .api_http import SDK_HTTP_ERROR_CODE
from .token_api import TokenAPI


def provision_req(
    token_api: TokenAPI,
) -> Callable[[Callable[[str], Response]], Result[Any, HTTPError]]:
    """
    Before every request, we make sure we use a valid access token.
    """

    def handle_request(request: Callable[[str], Response], token: str) -> Result[Any, HTTPError]:
        try:
            response = request(token)

            if response.ok:
                data = None
                if response.headers.get("content-type") == "application/json":
                    data = response.json()
                elif response.headers.get("content-type") == "application/octet-stream":
                    data = response.content
                else:
                    data = response.text

                return Success(data)
            else:
                body_error = response.text
                log.error(f"Request Error: {body_error}")
                return Failure(HTTPError(response.status_code, body_error))
        except requests.exceptions.RequestException as err:
            log.error(f"Request exception: {str(err)}")
            return Failure(HTTPError(SDK_HTTP_ERROR_CODE, str(err)))

    def req(request: Callable[[str], Response]) -> Result[Any, HTTPError]:
        access_token: Result[str, HTTPError]

        if token_api.access_token is not None:
            access_token = Success(token_api.access_token)
        else:
            access_token = token_api._request_access_token().map(lambda result: result["token"])

        return access_token.bind(lambda token: handle_request(request, token)).lash(
            lambda error: _renew_if_fails(
                token_api=token_api,
                request=lambda tkn: handle_request(request, tkn),
                http_error=error,
            )
        )

    return req


T = TypeVar("T")


def provision_token(
    token_api: TokenAPI,
) -> Callable[[Callable[[str], T]], Result[T, HTTPError]]:
    """
    Before every request, we make sure we use a valid access token.
    """

    def handle_request(request: Callable[[str], T], token: str) -> Result[T, HTTPError]:
        try:
            return Success(request(token))
        except requests.exceptions.RequestException as err:
            log.error(f"Request exception: {str(err)}")
            return Failure(HTTPError(SDK_HTTP_ERROR_CODE, str(err)))

    def req(request: Callable[[str], T]) -> Result[T, HTTPError]:
        access_token: Result[str, HTTPError]

        if token_api.access_token is not None:
            access_token = Success(token_api.access_token)
        else:
            access_token = token_api._request_access_token().map(lambda result: result["token"])

        return access_token.bind(lambda token: handle_request(request, token)).lash(
            lambda error: _renew_if_fails(
                token_api=token_api,
                request=lambda tkn: handle_request(request, tkn),
                http_error=error,
            )
        )

    return req


def _renew_if_fails(
    token_api: TokenAPI,
    request: Callable[[str], Result[T, HTTPError]],
    http_error: HTTPError,
) -> Result[T, HTTPError]:
    if http_error.status != 401:
        return Failure(http_error)

    if token_api.auto_renew:
        log.info("Auto-Renew, renewing the token...")
        token = token_api.renew_token()
        return request(token)
    else:
        return Failure(http_error)


def get_pdk_client(access_token: str, cfg: Configuration = config) -> ApiClient:
    """
    Constructs a Seaplane PDK ApiClient from the given access token.
    """
    from .. import __version__

    pdk_config = cfg.get_platform_configuration()
    pdk_config.access_token = access_token
    client = ApiClient(pdk_config)
    client.set_default_header("X-Seaplane-Sdk-Version", __version__)
    client.set_default_header("X-Seaplane-Pdk-Version", seaplane_framework.api.__version__)
    return client
