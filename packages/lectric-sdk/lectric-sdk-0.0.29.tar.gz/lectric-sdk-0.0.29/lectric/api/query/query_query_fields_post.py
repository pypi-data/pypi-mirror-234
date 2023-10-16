from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.query_spec import QuerySpec
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: QuerySpec,
) -> Dict[str, Any]:
    url = "{}/query/fields".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, HTTPValidationError, List[Any]]]:
    if response.status_code == 200:
        response_200 = cast(List[Any], response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, HTTPValidationError, List[Any]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: QuerySpec,
) -> Response[Union[Any, HTTPValidationError, List[Any]]]:
    """Query

     Query fields with an expression for exact result

    Args:
        json_body (QuerySpec):

    Returns:
        Response[Union[Any, HTTPValidationError, List[Any]]]
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
    json_body: QuerySpec,
) -> Optional[Union[Any, HTTPValidationError, List[Any]]]:
    """Query

     Query fields with an expression for exact result

    Args:
        json_body (QuerySpec):

    Returns:
        Response[Union[Any, HTTPValidationError, List[Any]]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: QuerySpec,
) -> Response[Union[Any, HTTPValidationError, List[Any]]]:
    """Query

     Query fields with an expression for exact result

    Args:
        json_body (QuerySpec):

    Returns:
        Response[Union[Any, HTTPValidationError, List[Any]]]
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
    json_body: QuerySpec,
) -> Optional[Union[Any, HTTPValidationError, List[Any]]]:
    """Query

     Query fields with an expression for exact result

    Args:
        json_body (QuerySpec):

    Returns:
        Response[Union[Any, HTTPValidationError, List[Any]]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
