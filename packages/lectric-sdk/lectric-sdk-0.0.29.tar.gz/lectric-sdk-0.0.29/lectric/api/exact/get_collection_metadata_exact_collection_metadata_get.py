from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...models.collection_metadata import CollectionMetadata
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    collection_name: str,
) -> Dict[str, Any]:
    url = "{}/exact/collection_metadata".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["collection_name"] = collection_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, CollectionMetadata, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = CollectionMetadata.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, CollectionMetadata, HTTPValidationError]]:
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
) -> Response[Union[Any, CollectionMetadata, HTTPValidationError]]:
    """Get Collection Metadata

    Args:
        collection_name (str):

    Returns:
        Response[Union[Any, CollectionMetadata, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        collection_name=collection_name,
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
) -> Optional[Union[Any, CollectionMetadata, HTTPValidationError]]:
    """Get Collection Metadata

    Args:
        collection_name (str):

    Returns:
        Response[Union[Any, CollectionMetadata, HTTPValidationError]]
    """

    return sync_detailed(
        client=client,
        collection_name=collection_name,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    collection_name: str,
) -> Response[Union[Any, CollectionMetadata, HTTPValidationError]]:
    """Get Collection Metadata

    Args:
        collection_name (str):

    Returns:
        Response[Union[Any, CollectionMetadata, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        collection_name=collection_name,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    collection_name: str,
) -> Optional[Union[Any, CollectionMetadata, HTTPValidationError]]:
    """Get Collection Metadata

    Args:
        collection_name (str):

    Returns:
        Response[Union[Any, CollectionMetadata, HTTPValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            collection_name=collection_name,
        )
    ).parsed
