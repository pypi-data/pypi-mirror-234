from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.create_deployed_api_client_request import CreateDeployedApiClientRequest
from ...models.deployed_api_client_create_response import (
    DeployedApiClientCreateResponse,
)
from ...types import Response


def _get_kwargs(
    pipeline_api_id: int,
    *,
    client: Client,
    json_body: CreateDeployedApiClientRequest,

) -> Dict[str, Any]:
    url = "{}/v1/pipelineApis/{pipelineApiId}/clients".format(
        client.base_url,pipelineApiId=pipeline_api_id)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, DeployedApiClientCreateResponse]]:
    if response.status_code == 201:
        response_201 = DeployedApiClientCreateResponse.from_dict(response.json())



        return response_201
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, DeployedApiClientCreateResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    pipeline_api_id: int,
    *,
    client: Client,
    json_body: CreateDeployedApiClientRequest,

) -> Response[Union[Any, DeployedApiClientCreateResponse]]:
    """Create a new client for a published data prep pipeline

     Create a new client to access and use a given published data prep pipeline api and returns its new
    credentials (client id and secret)

    Args:
        pipeline_api_id (int):
        json_body (CreateDeployedApiClientRequest):

    Returns:
        Response[Union[Any, DeployedApiClientCreateResponse]]
    """


    kwargs = _get_kwargs(
        pipeline_api_id=pipeline_api_id,
client=client,
json_body=json_body,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    pipeline_api_id: int,
    *,
    client: Client,
    json_body: CreateDeployedApiClientRequest,

) -> Optional[Union[Any, DeployedApiClientCreateResponse]]:
    """Create a new client for a published data prep pipeline

     Create a new client to access and use a given published data prep pipeline api and returns its new
    credentials (client id and secret)

    Args:
        pipeline_api_id (int):
        json_body (CreateDeployedApiClientRequest):

    Returns:
        Response[Union[Any, DeployedApiClientCreateResponse]]
    """


    return sync_detailed(
        pipeline_api_id=pipeline_api_id,
client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    pipeline_api_id: int,
    *,
    client: Client,
    json_body: CreateDeployedApiClientRequest,

) -> Response[Union[Any, DeployedApiClientCreateResponse]]:
    """Create a new client for a published data prep pipeline

     Create a new client to access and use a given published data prep pipeline api and returns its new
    credentials (client id and secret)

    Args:
        pipeline_api_id (int):
        json_body (CreateDeployedApiClientRequest):

    Returns:
        Response[Union[Any, DeployedApiClientCreateResponse]]
    """


    kwargs = _get_kwargs(
        pipeline_api_id=pipeline_api_id,
client=client,
json_body=json_body,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    pipeline_api_id: int,
    *,
    client: Client,
    json_body: CreateDeployedApiClientRequest,

) -> Optional[Union[Any, DeployedApiClientCreateResponse]]:
    """Create a new client for a published data prep pipeline

     Create a new client to access and use a given published data prep pipeline api and returns its new
    credentials (client id and secret)

    Args:
        pipeline_api_id (int):
        json_body (CreateDeployedApiClientRequest):

    Returns:
        Response[Union[Any, DeployedApiClientCreateResponse]]
    """


    return (await asyncio_detailed(
        pipeline_api_id=pipeline_api_id,
client=client,
json_body=json_body,

    )).parsed
