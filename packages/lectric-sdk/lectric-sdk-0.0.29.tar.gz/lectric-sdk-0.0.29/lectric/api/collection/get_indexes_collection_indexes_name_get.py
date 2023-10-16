from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    name: str,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/collection/indexes/{name}".format(client.base_url, name=name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, HTTPValidationError, List[str]]]:
    if response.status_code == 200:
        response_200 = cast(List[str], response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, HTTPValidationError, List[str]]]:
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
) -> Response[Union[Any, HTTPValidationError, List[str]]]:
    """Get Indexes

     Get field names of indexes associated with collection

    Args:
        name (str):

    Returns:
        Response[Union[Any, HTTPValidationError, List[str]]]
    """

    kwargs = _get_kwargs(
        name=name,
        client=client,
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
) -> Optional[Union[Any, HTTPValidationError, List[str]]]:
    """Get Indexes

     Get field names of indexes associated with collection

    Args:
        name (str):

    Returns:
        Response[Union[Any, HTTPValidationError, List[str]]]
    """

    return sync_detailed(
        name=name,
        client=client,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, HTTPValidationError, List[str]]]:
    """Get Indexes

     Get field names of indexes associated with collection

    Args:
        name (str):

    Returns:
        Response[Union[Any, HTTPValidationError, List[str]]]
    """

    kwargs = _get_kwargs(
        name=name,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, HTTPValidationError, List[str]]]:
    """Get Indexes

     Get field names of indexes associated with collection

    Args:
        name (str):

    Returns:
        Response[Union[Any, HTTPValidationError, List[str]]]
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
        )
    ).parsed
