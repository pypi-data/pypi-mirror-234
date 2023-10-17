from typing import Any, Dict

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    model_api_id: int,
    *,
    client: Client,

) -> Dict[str, Any]:
    url = "{}/v1/modelApis/{modelApiId}".format(
        client.base_url,modelApiId=model_api_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    

    return {
	    "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }




def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    model_api_id: int,
    *,
    client: Client,

) -> Response[Any]:
    """Deletes the specified published model

     Deletes the specified published model

    Args:
        model_api_id (int):

    Returns:
        Response[Any]
    """


    kwargs = _get_kwargs(
        model_api_id=model_api_id,
client=client,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    model_api_id: int,
    *,
    client: Client,

) -> Response[Any]:
    """Deletes the specified published model

     Deletes the specified published model

    Args:
        model_api_id (int):

    Returns:
        Response[Any]
    """


    kwargs = _get_kwargs(
        model_api_id=model_api_id,
client=client,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

