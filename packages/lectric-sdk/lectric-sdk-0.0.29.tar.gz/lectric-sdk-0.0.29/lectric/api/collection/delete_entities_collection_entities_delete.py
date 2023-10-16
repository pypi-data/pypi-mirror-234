from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: Union[List[int], List[str]],
    name: str,
) -> Dict[str, Any]:
    url = "{}/collection/entities".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["name"] = name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    if isinstance(json_body, list):
        json_json_body = json_body

    else:
        json_json_body = json_body

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
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
    json_body: Union[List[int], List[str]],
    name: str,
) -> Response[Union[Any, HTTPValidationError]]:
    """Delete Entities

     Delete entities in a collection

    Args:
        name (str):
        json_body (Union[List[int], List[str]]):

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        name=name,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: Union[List[int], List[str]],
    name: str,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Delete Entities

     Delete entities in a collection

    Args:
        name (str):
        json_body (Union[List[int], List[str]]):

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        name=name,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: Union[List[int], List[str]],
    name: str,
) -> Response[Union[Any, HTTPValidationError]]:
    """Delete Entities

     Delete entities in a collection

    Args:
        name (str):
        json_body (Union[List[int], List[str]]):

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        name=name,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: Union[List[int], List[str]],
    name: str,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Delete Entities

     Delete entities in a collection

    Args:
        name (str):
        json_body (Union[List[int], List[str]]):

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            name=name,
        )
    ).parsed
