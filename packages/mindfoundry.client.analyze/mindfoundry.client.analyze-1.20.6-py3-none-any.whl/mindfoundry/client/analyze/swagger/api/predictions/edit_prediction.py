from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.edit_prediction_request import EditPredictionRequest
from ...models.prediction_response import PredictionResponse
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    client: Client,
    json_body: EditPredictionRequest,

) -> Dict[str, Any]:
    url = "{}/v1/predictions/{id}".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, PredictionResponse]]:
    if response.status_code == 200:
        response_200 = PredictionResponse.from_dict(response.json())



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


def _build_response(*, response: httpx.Response) -> Response[Union[Any, PredictionResponse]]:
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
    json_body: EditPredictionRequest,

) -> Response[Union[Any, PredictionResponse]]:
    """Edit the name and description of the specified prediction

     Edit the name and description of the specified prediction

    Args:
        id (int):
        json_body (EditPredictionRequest):

    Returns:
        Response[Union[Any, PredictionResponse]]
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
    json_body: EditPredictionRequest,

) -> Optional[Union[Any, PredictionResponse]]:
    """Edit the name and description of the specified prediction

     Edit the name and description of the specified prediction

    Args:
        id (int):
        json_body (EditPredictionRequest):

    Returns:
        Response[Union[Any, PredictionResponse]]
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
    json_body: EditPredictionRequest,

) -> Response[Union[Any, PredictionResponse]]:
    """Edit the name and description of the specified prediction

     Edit the name and description of the specified prediction

    Args:
        id (int):
        json_body (EditPredictionRequest):

    Returns:
        Response[Union[Any, PredictionResponse]]
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
    json_body: EditPredictionRequest,

) -> Optional[Union[Any, PredictionResponse]]:
    """Edit the name and description of the specified prediction

     Edit the name and description of the specified prediction

    Args:
        id (int):
        json_body (EditPredictionRequest):

    Returns:
        Response[Union[Any, PredictionResponse]]
    """


    return (await asyncio_detailed(
        id=id,
client=client,
json_body=json_body,

    )).parsed
