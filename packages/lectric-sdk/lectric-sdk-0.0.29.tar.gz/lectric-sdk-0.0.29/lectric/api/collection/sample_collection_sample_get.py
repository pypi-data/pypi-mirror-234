from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.query_response import QueryResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    collection_name: str,
    max_samples: Union[Unset, None, int] = 20,
) -> Dict[str, Any]:
    url = "{}/collection/sample".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["collection_name"] = collection_name

    params["max_samples"] = max_samples

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, HTTPValidationError, QueryResponse]]:
    if response.status_code == 200:
        response_200 = QueryResponse.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, HTTPValidationError, QueryResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    collection_name: str,
    max_samples: Union[Unset, None, int] = 20,
) -> Response[Union[Any, HTTPValidationError, QueryResponse]]:
    """Sample

     Sample entries from a collection

    Args:
        collection_name (str):
        max_samples (Union[Unset, None, int]):  Default: 20.

    Returns:
        Response[Union[Any, HTTPValidationError, QueryResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        collection_name=collection_name,
        max_samples=max_samples,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    collection_name: str,
    max_samples: Union[Unset, None, int] = 20,
) -> Optional[Union[Any, HTTPValidationError, QueryResponse]]:
    """Sample

     Sample entries from a collection

    Args:
        collection_name (str):
        max_samples (Union[Unset, None, int]):  Default: 20.

    Returns:
        Response[Union[Any, HTTPValidationError, QueryResponse]]
    """

    return sync_detailed(
        client=client,
        collection_name=collection_name,
        max_samples=max_samples,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    collection_name: str,
    max_samples: Union[Unset, None, int] = 20,
) -> Response[Union[Any, HTTPValidationError, QueryResponse]]:
    """Sample

     Sample entries from a collection

    Args:
        collection_name (str):
        max_samples (Union[Unset, None, int]):  Default: 20.

    Returns:
        Response[Union[Any, HTTPValidationError, QueryResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        collection_name=collection_name,
        max_samples=max_samples,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    collection_name: str,
    max_samples: Union[Unset, None, int] = 20,
) -> Optional[Union[Any, HTTPValidationError, QueryResponse]]:
    """Sample

     Sample entries from a collection

    Args:
        collection_name (str):
        max_samples (Union[Unset, None, int]):  Default: 20.

    Returns:
        Response[Union[Any, HTTPValidationError, QueryResponse]]
    """

    return (
        await asyncio_detailed(
            client=client,
            collection_name=collection_name,
            max_samples=max_samples,
        )
    ).parsed
