from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    collection_name: str,
    field_name: str,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/index/{collection_name}/{field_name}".format(
        client.base_url, collection_name=collection_name, field_name=field_name
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = cast(Any, response.json())
        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    collection_name: str,
    field_name: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, HTTPValidationError]]:
    """Delete

     Destroy an index

    Args:
        collection_name (str):
        field_name (str):

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        collection_name=collection_name,
        field_name=field_name,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    collection_name: str,
    field_name: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Delete

     Destroy an index

    Args:
        collection_name (str):
        field_name (str):

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    return sync_detailed(
        collection_name=collection_name,
        field_name=field_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    collection_name: str,
    field_name: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, HTTPValidationError]]:
    """Delete

     Destroy an index

    Args:
        collection_name (str):
        field_name (str):

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        collection_name=collection_name,
        field_name=field_name,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    collection_name: str,
    field_name: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Delete

     Destroy an index

    Args:
        collection_name (str):
        field_name (str):

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    return (
        await asyncio_detailed(
            collection_name=collection_name,
            field_name=field_name,
            client=client,
        )
    ).parsed
