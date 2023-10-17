from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.id_response import IdResponse
from ...models.save_model_results_request import SaveModelResultsRequest
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    client: Client,
    json_body: SaveModelResultsRequest,

) -> Dict[str, Any]:
    url = "{}/v1/models/{id}/results/save".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, IdResponse]]:
    if response.status_code == 201:
        response_201 = IdResponse.from_dict(response.json())



        return response_201
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


def _build_response(*, response: httpx.Response) -> Response[Union[Any, IdResponse]]:
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
    json_body: SaveModelResultsRequest,

) -> Response[Union[Any, IdResponse]]:
    """Save the results of the specified model as a new data set

     Save the results of the specified model as a new data set - For classification & regression this
    result is the result of hold-out test, for clustering it is the clustered data.

    Args:
        id (int):
        json_body (SaveModelResultsRequest):

    Returns:
        Response[Union[Any, IdResponse]]
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
    json_body: SaveModelResultsRequest,

) -> Optional[Union[Any, IdResponse]]:
    """Save the results of the specified model as a new data set

     Save the results of the specified model as a new data set - For classification & regression this
    result is the result of hold-out test, for clustering it is the clustered data.

    Args:
        id (int):
        json_body (SaveModelResultsRequest):

    Returns:
        Response[Union[Any, IdResponse]]
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
    json_body: SaveModelResultsRequest,

) -> Response[Union[Any, IdResponse]]:
    """Save the results of the specified model as a new data set

     Save the results of the specified model as a new data set - For classification & regression this
    result is the result of hold-out test, for clustering it is the clustered data.

    Args:
        id (int):
        json_body (SaveModelResultsRequest):

    Returns:
        Response[Union[Any, IdResponse]]
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
    json_body: SaveModelResultsRequest,

) -> Optional[Union[Any, IdResponse]]:
    """Save the results of the specified model as a new data set

     Save the results of the specified model as a new data set - For classification & regression this
    result is the result of hold-out test, for clustering it is the clustered data.

    Args:
        id (int):
        json_body (SaveModelResultsRequest):

    Returns:
        Response[Union[Any, IdResponse]]
    """


    return (await asyncio_detailed(
        id=id,
client=client,
json_body=json_body,

    )).parsed
