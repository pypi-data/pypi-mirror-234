from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.index_in_spec import IndexInSpec
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: IndexInSpec,
) -> Dict[str, Any]:
    url = "{}/index/create".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
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
    *,
    client: AuthenticatedClient,
    json_body: IndexInSpec,
) -> Response[Union[Any, HTTPValidationError]]:
    """Create

     Create an index on field name specified (must be defined within schema first)

    Args:
        json_body (IndexInSpec):

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: IndexInSpec,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Create

     Create an index on field name specified (must be defined within schema first)

    Args:
        json_body (IndexInSpec):

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: IndexInSpec,
) -> Response[Union[Any, HTTPValidationError]]:
    """Create

     Create an index on field name specified (must be defined within schema first)

    Args:
        json_body (IndexInSpec):

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: IndexInSpec,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Create

     Create an index on field name specified (must be defined within schema first)

    Args:
        json_body (IndexInSpec):

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
