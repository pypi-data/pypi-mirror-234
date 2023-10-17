from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.test_response import TestResponse
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    client: Client,

) -> Dict[str, Any]:
    url = "{}/v1/tests/{id}".format(
        client.base_url,id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    

    return {
	    "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, TestResponse]]:
    if response.status_code == 200:
        response_200 = TestResponse.from_dict(response.json())



        return response_200
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, TestResponse]]:
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

) -> Response[Union[Any, TestResponse]]:
    """Gets an overview of the test

     Gets general information about the test, including the current status

    Args:
        id (int):

    Returns:
        Response[Union[Any, TestResponse]]
    """


    kwargs = _get_kwargs(
        id=id,
client=client,

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

) -> Optional[Union[Any, TestResponse]]:
    """Gets an overview of the test

     Gets general information about the test, including the current status

    Args:
        id (int):

    Returns:
        Response[Union[Any, TestResponse]]
    """


    return sync_detailed(
        id=id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: int,
    *,
    client: Client,

) -> Response[Union[Any, TestResponse]]:
    """Gets an overview of the test

     Gets general information about the test, including the current status

    Args:
        id (int):

    Returns:
        Response[Union[Any, TestResponse]]
    """


    kwargs = _get_kwargs(
        id=id,
client=client,

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

) -> Optional[Union[Any, TestResponse]]:
    """Gets an overview of the test

     Gets general information about the test, including the current status

    Args:
        id (int):

    Returns:
        Response[Union[Any, TestResponse]]
    """


    return (await asyncio_detailed(
        id=id,
client=client,

    )).parsed
