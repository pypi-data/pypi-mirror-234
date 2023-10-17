from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.deployed_pipeline_api_response import DeployedPipelineApiResponse
from ...models.edit_deployed_pipeline_api_request import EditDeployedPipelineApiRequest
from ...types import Response


def _get_kwargs(
    pipeline_api_id: int,
    *,
    client: Client,
    json_body: EditDeployedPipelineApiRequest,

) -> Dict[str, Any]:
    url = "{}/v1/pipelineApis/{pipelineApiId}".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, DeployedPipelineApiResponse]]:
    if response.status_code == 200:
        response_200 = DeployedPipelineApiResponse.from_dict(response.json())



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


def _build_response(*, response: httpx.Response) -> Response[Union[Any, DeployedPipelineApiResponse]]:
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
    json_body: EditDeployedPipelineApiRequest,

) -> Response[Union[Any, DeployedPipelineApiResponse]]:
    """Edit the specified published data prep pipeline

     Edits the specified published data prep pipeline

    Args:
        pipeline_api_id (int):
        json_body (EditDeployedPipelineApiRequest):

    Returns:
        Response[Union[Any, DeployedPipelineApiResponse]]
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
    json_body: EditDeployedPipelineApiRequest,

) -> Optional[Union[Any, DeployedPipelineApiResponse]]:
    """Edit the specified published data prep pipeline

     Edits the specified published data prep pipeline

    Args:
        pipeline_api_id (int):
        json_body (EditDeployedPipelineApiRequest):

    Returns:
        Response[Union[Any, DeployedPipelineApiResponse]]
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
    json_body: EditDeployedPipelineApiRequest,

) -> Response[Union[Any, DeployedPipelineApiResponse]]:
    """Edit the specified published data prep pipeline

     Edits the specified published data prep pipeline

    Args:
        pipeline_api_id (int):
        json_body (EditDeployedPipelineApiRequest):

    Returns:
        Response[Union[Any, DeployedPipelineApiResponse]]
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
    json_body: EditDeployedPipelineApiRequest,

) -> Optional[Union[Any, DeployedPipelineApiResponse]]:
    """Edit the specified published data prep pipeline

     Edits the specified published data prep pipeline

    Args:
        pipeline_api_id (int):
        json_body (EditDeployedPipelineApiRequest):

    Returns:
        Response[Union[Any, DeployedPipelineApiResponse]]
    """


    return (await asyncio_detailed(
        pipeline_api_id=pipeline_api_id,
client=client,
json_body=json_body,

    )).parsed
