from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.create_file_data_set_request import CreateFileDataSetRequest
from ...models.future import Future
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    multipart_data: CreateFileDataSetRequest,

) -> Dict[str, Any]:
    url = "{}/v1/dataSets/file".format(
        client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    multipart_multipart_data = multipart_data.to_multipart()




    return {
	    "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_multipart_data,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, Future]]:
    if response.status_code == 201:
        response_201 = Future.from_dict(response.json())



        return response_201
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, Future]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    multipart_data: CreateFileDataSetRequest,

) -> Response[Union[Any, Future]]:
    """Create a new data set from uploaded file

     Your data will start being imported immediately. The response will contain a `futureId` which you
    can use with the `/futures` endpoint to check the progress of your import. Upon completion the
    future will give you information about the resulting data set.

    Args:
        multipart_data (CreateFileDataSetRequest):

    Returns:
        Response[Union[Any, Future]]
    """


    kwargs = _get_kwargs(
        client=client,
multipart_data=multipart_data,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,
    multipart_data: CreateFileDataSetRequest,

) -> Optional[Union[Any, Future]]:
    """Create a new data set from uploaded file

     Your data will start being imported immediately. The response will contain a `futureId` which you
    can use with the `/futures` endpoint to check the progress of your import. Upon completion the
    future will give you information about the resulting data set.

    Args:
        multipart_data (CreateFileDataSetRequest):

    Returns:
        Response[Union[Any, Future]]
    """


    return sync_detailed(
        client=client,
multipart_data=multipart_data,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    multipart_data: CreateFileDataSetRequest,

) -> Response[Union[Any, Future]]:
    """Create a new data set from uploaded file

     Your data will start being imported immediately. The response will contain a `futureId` which you
    can use with the `/futures` endpoint to check the progress of your import. Upon completion the
    future will give you information about the resulting data set.

    Args:
        multipart_data (CreateFileDataSetRequest):

    Returns:
        Response[Union[Any, Future]]
    """


    kwargs = _get_kwargs(
        client=client,
multipart_data=multipart_data,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    *,
    client: Client,
    multipart_data: CreateFileDataSetRequest,

) -> Optional[Union[Any, Future]]:
    """Create a new data set from uploaded file

     Your data will start being imported immediately. The response will contain a `futureId` which you
    can use with the `/futures` endpoint to check the progress of your import. Upon completion the
    future will give you information about the resulting data set.

    Args:
        multipart_data (CreateFileDataSetRequest):

    Returns:
        Response[Union[Any, Future]]
    """


    return (await asyncio_detailed(
        client=client,
multipart_data=multipart_data,

    )).parsed
