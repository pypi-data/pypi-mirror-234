from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...models.body_ingest_w_file_ingest_file_post import BodyIngestWFileIngestFilePost
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    multipart_data: BodyIngestWFileIngestFilePost,
    collection_name: str,
    json_input_data: str,
) -> Dict[str, Any]:
    url = "{}/ingest/file".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["collection_name"] = collection_name

    params["json_input_data"] = json_input_data

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_multipart_data,
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
    multipart_data: BodyIngestWFileIngestFilePost,
    collection_name: str,
    json_input_data: str,
) -> Response[Union[Any, HTTPValidationError]]:
    """Ingest W File

     Ingest one element with a file to be stored into a collection

    Args:
        collection_name (str):
        json_input_data (str):
        multipart_data (BodyIngestWFileIngestFilePost):

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        collection_name=collection_name,
        json_input_data=json_input_data,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    multipart_data: BodyIngestWFileIngestFilePost,
    collection_name: str,
    json_input_data: str,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Ingest W File

     Ingest one element with a file to be stored into a collection

    Args:
        collection_name (str):
        json_input_data (str):
        multipart_data (BodyIngestWFileIngestFilePost):

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    return sync_detailed(
        client=client,
        multipart_data=multipart_data,
        collection_name=collection_name,
        json_input_data=json_input_data,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    multipart_data: BodyIngestWFileIngestFilePost,
    collection_name: str,
    json_input_data: str,
) -> Response[Union[Any, HTTPValidationError]]:
    """Ingest W File

     Ingest one element with a file to be stored into a collection

    Args:
        collection_name (str):
        json_input_data (str):
        multipart_data (BodyIngestWFileIngestFilePost):

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        collection_name=collection_name,
        json_input_data=json_input_data,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    multipart_data: BodyIngestWFileIngestFilePost,
    collection_name: str,
    json_input_data: str,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Ingest W File

     Ingest one element with a file to be stored into a collection

    Args:
        collection_name (str):
        json_input_data (str):
        multipart_data (BodyIngestWFileIngestFilePost):

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            multipart_data=multipart_data,
            collection_name=collection_name,
            json_input_data=json_input_data,
        )
    ).parsed
