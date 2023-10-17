from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.data_set_response import DataSetResponse
from ...models.edit_data_set_request import EditDataSetRequest
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    client: Client,
    json_body: EditDataSetRequest,

) -> Dict[str, Any]:
    url = "{}/v1/dataSets/{id}".format(
        client.base_url,id=id)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, DataSetResponse]]:
    if response.status_code == 200:
        response_200 = DataSetResponse.from_dict(response.json())



        return response_200
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, DataSetResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    id: int,
    *,
    client: Client,
    json_body: EditDataSetRequest,

) -> Response[Union[Any, DataSetResponse]]:
    """Edit the specified data set

     Edits the specified data set

    Args:
        id (int):
        json_body (EditDataSetRequest):

    Returns:
        Response[Union[Any, DataSetResponse]]
    """


    kwargs = _get_kwargs(
        id=id,
client=client,
json_body=json_body,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    id: int,
    *,
    client: Client,
    json_body: EditDataSetRequest,

) -> Optional[Union[Any, DataSetResponse]]:
    """Edit the specified data set

     Edits the specified data set

    Args:
        id (int):
        json_body (EditDataSetRequest):

    Returns:
        Response[Union[Any, DataSetResponse]]
    """


    return sync_detailed(
        id=id,
client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    id: int,
    *,
    client: Client,
    json_body: EditDataSetRequest,

) -> Response[Union[Any, DataSetResponse]]:
    """Edit the specified data set

     Edits the specified data set

    Args:
        id (int):
        json_body (EditDataSetRequest):

    Returns:
        Response[Union[Any, DataSetResponse]]
    """


    kwargs = _get_kwargs(
        id=id,
client=client,
json_body=json_body,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    id: int,
    *,
    client: Client,
    json_body: EditDataSetRequest,

) -> Optional[Union[Any, DataSetResponse]]:
    """Edit the specified data set

     Edits the specified data set

    Args:
        id (int):
        json_body (EditDataSetRequest):

    Returns:
        Response[Union[Any, DataSetResponse]]
    """


    return (await asyncio_detailed(
        id=id,
client=client,
json_body=json_body,

    )).parsed
