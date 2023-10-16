from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    name: str,
    limit: Union[Unset, None, int] = UNSET,
    total_only: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/exact/counter/dupes".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["name"] = name

    params["limit"] = limit

    params["total_only"] = total_only

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, Union[List[List[Any]], int]]]:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> Union[List[List[Any]], int]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                response_200_type_0 = UNSET
                _response_200_type_0 = data
                for response_200_type_0_item_data in _response_200_type_0:
                    response_200_type_0_item = cast(List[Any], response_200_type_0_item_data)

                    response_200_type_0.append(response_200_type_0_item)

                return response_200_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[List[Any]], int], data)

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[Any, HTTPValidationError, Union[List[List[Any]], int]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    name: str,
    limit: Union[Unset, None, int] = UNSET,
    total_only: Union[Unset, None, bool] = False,
) -> Response[Union[Any, HTTPValidationError, Union[List[List[Any]], int]]]:
    """Dupes List

    Args:
        name (str):
        limit (Union[Unset, None, int]):
        total_only (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, HTTPValidationError, Union[List[List[Any]], int]]]
    """

    kwargs = _get_kwargs(
        client=client,
        name=name,
        limit=limit,
        total_only=total_only,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    name: str,
    limit: Union[Unset, None, int] = UNSET,
    total_only: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, HTTPValidationError, Union[List[List[Any]], int]]]:
    """Dupes List

    Args:
        name (str):
        limit (Union[Unset, None, int]):
        total_only (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, HTTPValidationError, Union[List[List[Any]], int]]]
    """

    return sync_detailed(
        client=client,
        name=name,
        limit=limit,
        total_only=total_only,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    name: str,
    limit: Union[Unset, None, int] = UNSET,
    total_only: Union[Unset, None, bool] = False,
) -> Response[Union[Any, HTTPValidationError, Union[List[List[Any]], int]]]:
    """Dupes List

    Args:
        name (str):
        limit (Union[Unset, None, int]):
        total_only (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, HTTPValidationError, Union[List[List[Any]], int]]]
    """

    kwargs = _get_kwargs(
        client=client,
        name=name,
        limit=limit,
        total_only=total_only,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    name: str,
    limit: Union[Unset, None, int] = UNSET,
    total_only: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, HTTPValidationError, Union[List[List[Any]], int]]]:
    """Dupes List

    Args:
        name (str):
        limit (Union[Unset, None, int]):
        total_only (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, HTTPValidationError, Union[List[List[Any]], int]]]
    """

    return (
        await asyncio_detailed(
            client=client,
            name=name,
            limit=limit,
            total_only=total_only,
        )
    ).parsed
