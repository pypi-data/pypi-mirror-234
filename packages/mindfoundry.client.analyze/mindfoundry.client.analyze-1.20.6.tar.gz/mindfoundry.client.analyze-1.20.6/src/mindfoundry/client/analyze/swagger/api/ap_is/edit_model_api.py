from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.deployed_model_api_response import DeployedModelApiResponse
from ...models.edit_deployed_model_api_request import EditDeployedModelApiRequest
from ...types import Response


def _get_kwargs(
    model_api_id: int,
    *,
    client: Client,
    json_body: EditDeployedModelApiRequest,

) -> Dict[str, Any]:
    url = "{}/v1/modelApis/{modelApiId}".format(
        client.base_url,modelApiId=model_api_id)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, DeployedModelApiResponse]]:
    if response.status_code == 200:
        response_200 = DeployedModelApiResponse.from_dict(response.json())



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


def _build_response(*, response: httpx.Response) -> Response[Union[Any, DeployedModelApiResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    model_api_id: int,
    *,
    client: Client,
    json_body: EditDeployedModelApiRequest,

) -> Response[Union[Any, DeployedModelApiResponse]]:
    """Edit the specified published model

     Edits the specified published model

    Args:
        model_api_id (int):
        json_body (EditDeployedModelApiRequest):

    Returns:
        Response[Union[Any, DeployedModelApiResponse]]
    """


    kwargs = _get_kwargs(
        model_api_id=model_api_id,
client=client,
json_body=json_body,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    model_api_id: int,
    *,
    client: Client,
    json_body: EditDeployedModelApiRequest,

) -> Optional[Union[Any, DeployedModelApiResponse]]:
    """Edit the specified published model

     Edits the specified published model

    Args:
        model_api_id (int):
        json_body (EditDeployedModelApiRequest):

    Returns:
        Response[Union[Any, DeployedModelApiResponse]]
    """


    return sync_detailed(
        model_api_id=model_api_id,
client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    model_api_id: int,
    *,
    client: Client,
    json_body: EditDeployedModelApiRequest,

) -> Response[Union[Any, DeployedModelApiResponse]]:
    """Edit the specified published model

     Edits the specified published model

    Args:
        model_api_id (int):
        json_body (EditDeployedModelApiRequest):

    Returns:
        Response[Union[Any, DeployedModelApiResponse]]
    """


    kwargs = _get_kwargs(
        model_api_id=model_api_id,
client=client,
json_body=json_body,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    model_api_id: int,
    *,
    client: Client,
    json_body: EditDeployedModelApiRequest,

) -> Optional[Union[Any, DeployedModelApiResponse]]:
    """Edit the specified published model

     Edits the specified published model

    Args:
        model_api_id (int):
        json_body (EditDeployedModelApiRequest):

    Returns:
        Response[Union[Any, DeployedModelApiResponse]]
    """


    return (await asyncio_detailed(
        model_api_id=model_api_id,
client=client,
json_body=json_body,

    )).parsed
