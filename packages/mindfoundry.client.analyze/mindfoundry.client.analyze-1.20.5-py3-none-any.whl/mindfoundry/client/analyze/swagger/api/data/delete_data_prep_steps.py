from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.delete_data_prep_steps_request import DeleteDataPrepStepsRequest
from ...models.future import Future
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    client: Client,
    json_body: DeleteDataPrepStepsRequest,

) -> Dict[str, Any]:
    url = "{}/v1/dataSets/{id}/dataPrepSteps".format(
        client.base_url,id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    json_json_body = json_body.to_dict()



    

    return {
	    "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, Future]]:
    if response.status_code == 200:
        response_200 = Future.from_dict(response.json())



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


def _build_response(*, response: httpx.Response) -> Response[Union[Any, Future]]:
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
    json_body: DeleteDataPrepStepsRequest,

) -> Response[Union[Any, Future]]:
    """Deletes the specified data prep steps from the dataset

     Deletes the specified data prep steps from the dataset. This may take some time as later steps need
    to be reapplied so a future is returned.

    Args:
        id (int):
        json_body (DeleteDataPrepStepsRequest):

    Returns:
        Response[Union[Any, Future]]
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
    json_body: DeleteDataPrepStepsRequest,

) -> Optional[Union[Any, Future]]:
    """Deletes the specified data prep steps from the dataset

     Deletes the specified data prep steps from the dataset. This may take some time as later steps need
    to be reapplied so a future is returned.

    Args:
        id (int):
        json_body (DeleteDataPrepStepsRequest):

    Returns:
        Response[Union[Any, Future]]
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
    json_body: DeleteDataPrepStepsRequest,

) -> Response[Union[Any, Future]]:
    """Deletes the specified data prep steps from the dataset

     Deletes the specified data prep steps from the dataset. This may take some time as later steps need
    to be reapplied so a future is returned.

    Args:
        id (int):
        json_body (DeleteDataPrepStepsRequest):

    Returns:
        Response[Union[Any, Future]]
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
    json_body: DeleteDataPrepStepsRequest,

) -> Optional[Union[Any, Future]]:
    """Deletes the specified data prep steps from the dataset

     Deletes the specified data prep steps from the dataset. This may take some time as later steps need
    to be reapplied so a future is returned.

    Args:
        id (int):
        json_body (DeleteDataPrepStepsRequest):

    Returns:
        Response[Union[Any, Future]]
    """


    return (await asyncio_detailed(
        id=id,
client=client,
json_body=json_body,

    )).parsed
