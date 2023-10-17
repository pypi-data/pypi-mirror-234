from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.deployed_api_client_response import DeployedApiClientResponse
from ...types import Response


def _get_kwargs(
    pipeline_api_id: int,
    client_id: str,
    *,
    client: Client,

) -> Dict[str, Any]:
    url = "{}/v1/pipelineApis/{pipelineApiId}/clients/{clientId}".format(
        client.base_url,pipelineApiId=pipeline_api_id,clientId=client_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    

    return {
	    "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, DeployedApiClientResponse]]:
    if response.status_code == 200:
        response_200 = DeployedApiClientResponse.from_dict(response.json())



        return response_200
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, DeployedApiClientResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    pipeline_api_id: int,
    client_id: str,
    *,
    client: Client,

) -> Response[Union[Any, DeployedApiClientResponse]]:
    """Gets an overview of the published data prep pipeline api client

     Gets an overview of the published data prep pipeline api client

    Args:
        pipeline_api_id (int):
        client_id (str):

    Returns:
        Response[Union[Any, DeployedApiClientResponse]]
    """


    kwargs = _get_kwargs(
        pipeline_api_id=pipeline_api_id,
client_id=client_id,
client=client,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    pipeline_api_id: int,
    client_id: str,
    *,
    client: Client,

) -> Optional[Union[Any, DeployedApiClientResponse]]:
    """Gets an overview of the published data prep pipeline api client

     Gets an overview of the published data prep pipeline api client

    Args:
        pipeline_api_id (int):
        client_id (str):

    Returns:
        Response[Union[Any, DeployedApiClientResponse]]
    """


    return sync_detailed(
        pipeline_api_id=pipeline_api_id,
client_id=client_id,
client=client,

    ).parsed

async def asyncio_detailed(
    pipeline_api_id: int,
    client_id: str,
    *,
    client: Client,

) -> Response[Union[Any, DeployedApiClientResponse]]:
    """Gets an overview of the published data prep pipeline api client

     Gets an overview of the published data prep pipeline api client

    Args:
        pipeline_api_id (int):
        client_id (str):

    Returns:
        Response[Union[Any, DeployedApiClientResponse]]
    """


    kwargs = _get_kwargs(
        pipeline_api_id=pipeline_api_id,
client_id=client_id,
client=client,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    pipeline_api_id: int,
    client_id: str,
    *,
    client: Client,

) -> Optional[Union[Any, DeployedApiClientResponse]]:
    """Gets an overview of the published data prep pipeline api client

     Gets an overview of the published data prep pipeline api client

    Args:
        pipeline_api_id (int):
        client_id (str):

    Returns:
        Response[Union[Any, DeployedApiClientResponse]]
    """


    return (await asyncio_detailed(
        pipeline_api_id=pipeline_api_id,
client_id=client_id,
client=client,

    )).parsed
