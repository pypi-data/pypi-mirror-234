from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...models.collection import Collection
from ...models.collection_in_spec import CollectionInSpec
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: CollectionInSpec,
    with_reverse_lookup: Union[Unset, None, bool] = False,
    with_dupe_counter: Union[Unset, None, bool] = False,
    hash_algo: Union[Unset, None, str] = "md5",
) -> Dict[str, Any]:
    url = "{}/exact/create/collection".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["with_reverse_lookup"] = with_reverse_lookup

    params["with_dupe_counter"] = with_dupe_counter

    params["hash_algo"] = hash_algo

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, Collection, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = Collection.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, Collection, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: CollectionInSpec,
    with_reverse_lookup: Union[Unset, None, bool] = False,
    with_dupe_counter: Union[Unset, None, bool] = False,
    hash_algo: Union[Unset, None, str] = "md5",
) -> Response[Union[Any, Collection, HTTPValidationError]]:
    """Create Collection

     Create a collection by name with a specific schema

    Args:
        with_reverse_lookup (Union[Unset, None, bool]):
        with_dupe_counter (Union[Unset, None, bool]):
        hash_algo (Union[Unset, None, str]):  Default: 'md5'.
        json_body (CollectionInSpec):

    Returns:
        Response[Union[Any, Collection, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        with_reverse_lookup=with_reverse_lookup,
        with_dupe_counter=with_dupe_counter,
        hash_algo=hash_algo,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: CollectionInSpec,
    with_reverse_lookup: Union[Unset, None, bool] = False,
    with_dupe_counter: Union[Unset, None, bool] = False,
    hash_algo: Union[Unset, None, str] = "md5",
) -> Optional[Union[Any, Collection, HTTPValidationError]]:
    """Create Collection

     Create a collection by name with a specific schema

    Args:
        with_reverse_lookup (Union[Unset, None, bool]):
        with_dupe_counter (Union[Unset, None, bool]):
        hash_algo (Union[Unset, None, str]):  Default: 'md5'.
        json_body (CollectionInSpec):

    Returns:
        Response[Union[Any, Collection, HTTPValidationError]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        with_reverse_lookup=with_reverse_lookup,
        with_dupe_counter=with_dupe_counter,
        hash_algo=hash_algo,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: CollectionInSpec,
    with_reverse_lookup: Union[Unset, None, bool] = False,
    with_dupe_counter: Union[Unset, None, bool] = False,
    hash_algo: Union[Unset, None, str] = "md5",
) -> Response[Union[Any, Collection, HTTPValidationError]]:
    """Create Collection

     Create a collection by name with a specific schema

    Args:
        with_reverse_lookup (Union[Unset, None, bool]):
        with_dupe_counter (Union[Unset, None, bool]):
        hash_algo (Union[Unset, None, str]):  Default: 'md5'.
        json_body (CollectionInSpec):

    Returns:
        Response[Union[Any, Collection, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        with_reverse_lookup=with_reverse_lookup,
        with_dupe_counter=with_dupe_counter,
        hash_algo=hash_algo,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: CollectionInSpec,
    with_reverse_lookup: Union[Unset, None, bool] = False,
    with_dupe_counter: Union[Unset, None, bool] = False,
    hash_algo: Union[Unset, None, str] = "md5",
) -> Optional[Union[Any, Collection, HTTPValidationError]]:
    """Create Collection

     Create a collection by name with a specific schema

    Args:
        with_reverse_lookup (Union[Unset, None, bool]):
        with_dupe_counter (Union[Unset, None, bool]):
        hash_algo (Union[Unset, None, str]):  Default: 'md5'.
        json_body (CollectionInSpec):

    Returns:
        Response[Union[Any, Collection, HTTPValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            with_reverse_lookup=with_reverse_lookup,
            with_dupe_counter=with_dupe_counter,
            hash_algo=hash_algo,
        )
    ).parsed
