from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    path: str,
    access_duration_sec: Union[Unset, None, float] = 3600.0,
) -> Dict[str, Any]:
    url = "{}/collection/get_url".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["path"] = path

    params["access_duration_sec"] = access_duration_sec

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, HTTPValidationError, str]]:
    if response.status_code == 200:
        response_200 = cast(str, response.json())
        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, HTTPValidationError, str]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    path: str,
    access_duration_sec: Union[Unset, None, float] = 3600.0,
) -> Response[Union[Any, HTTPValidationError, str]]:
    """Get Url

    Args:
        path (str):
        access_duration_sec (Union[Unset, None, float]):  Default: 3600.0.

    Returns:
        Response[Union[Any, HTTPValidationError, str]]
    """

    kwargs = _get_kwargs(
        client=client,
        path=path,
        access_duration_sec=access_duration_sec,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    path: str,
    access_duration_sec: Union[Unset, None, float] = 3600.0,
) -> Optional[Union[Any, HTTPValidationError, str]]:
    """Get Url

    Args:
        path (str):
        access_duration_sec (Union[Unset, None, float]):  Default: 3600.0.

    Returns:
        Response[Union[Any, HTTPValidationError, str]]
    """

    return sync_detailed(
        client=client,
        path=path,
        access_duration_sec=access_duration_sec,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    path: str,
    access_duration_sec: Union[Unset, None, float] = 3600.0,
) -> Response[Union[Any, HTTPValidationError, str]]:
    """Get Url

    Args:
        path (str):
        access_duration_sec (Union[Unset, None, float]):  Default: 3600.0.

    Returns:
        Response[Union[Any, HTTPValidationError, str]]
    """

    kwargs = _get_kwargs(
        client=client,
        path=path,
        access_duration_sec=access_duration_sec,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    path: str,
    access_duration_sec: Union[Unset, None, float] = 3600.0,
) -> Optional[Union[Any, HTTPValidationError, str]]:
    """Get Url

    Args:
        path (str):
        access_duration_sec (Union[Unset, None, float]):  Default: 3600.0.

    Returns:
        Response[Union[Any, HTTPValidationError, str]]
    """

    return (
        await asyncio_detailed(
            client=client,
            path=path,
            access_duration_sec=access_duration_sec,
        )
    ).parsed
