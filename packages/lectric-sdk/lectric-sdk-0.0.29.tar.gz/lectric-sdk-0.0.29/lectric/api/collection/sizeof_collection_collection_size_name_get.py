from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    name: str,
    *,
    client: AuthenticatedClient,
    exact: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/collection/size/{name}".format(client.base_url, name=name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["exact"] = exact

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, HTTPValidationError, int]]:
    if response.status_code == 200:
        response_200 = cast(int, response.json())
        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, HTTPValidationError, int]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    name: str,
    *,
    client: AuthenticatedClient,
    exact: Union[Unset, None, bool] = False,
) -> Response[Union[Any, HTTPValidationError, int]]:
    """Sizeof Collection

     Get the number of entities in a collection

    Args:
        name (str):
        exact (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, HTTPValidationError, int]]
    """

    kwargs = _get_kwargs(
        name=name,
        client=client,
        exact=exact,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient,
    exact: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, HTTPValidationError, int]]:
    """Sizeof Collection

     Get the number of entities in a collection

    Args:
        name (str):
        exact (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, HTTPValidationError, int]]
    """

    return sync_detailed(
        name=name,
        client=client,
        exact=exact,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient,
    exact: Union[Unset, None, bool] = False,
) -> Response[Union[Any, HTTPValidationError, int]]:
    """Sizeof Collection

     Get the number of entities in a collection

    Args:
        name (str):
        exact (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, HTTPValidationError, int]]
    """

    kwargs = _get_kwargs(
        name=name,
        client=client,
        exact=exact,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient,
    exact: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, HTTPValidationError, int]]:
    """Sizeof Collection

     Get the number of entities in a collection

    Args:
        name (str):
        exact (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, HTTPValidationError, int]]
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            exact=exact,
        )
    ).parsed
