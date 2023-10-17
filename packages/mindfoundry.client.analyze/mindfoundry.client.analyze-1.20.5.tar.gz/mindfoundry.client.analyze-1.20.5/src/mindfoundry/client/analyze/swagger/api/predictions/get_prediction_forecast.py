from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.prediction_forecast_response import PredictionForecastResponse
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    client: Client,

) -> Dict[str, Any]:
    url = "{}/v1/predictions/{id}/forecast".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, PredictionForecastResponse]]:
    if response.status_code == 200:
        response_200 = PredictionForecastResponse.from_dict(response.json())



        return response_200
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, PredictionForecastResponse]]:
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

) -> Response[Union[Any, PredictionForecastResponse]]:
    """Gets the forecast produced by a prediction

     Obtains the forecast information for the specified prediction if available

    Args:
        id (int):

    Returns:
        Response[Union[Any, PredictionForecastResponse]]
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

) -> Optional[Union[Any, PredictionForecastResponse]]:
    """Gets the forecast produced by a prediction

     Obtains the forecast information for the specified prediction if available

    Args:
        id (int):

    Returns:
        Response[Union[Any, PredictionForecastResponse]]
    """


    return sync_detailed(
        id=id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: int,
    *,
    client: Client,

) -> Response[Union[Any, PredictionForecastResponse]]:
    """Gets the forecast produced by a prediction

     Obtains the forecast information for the specified prediction if available

    Args:
        id (int):

    Returns:
        Response[Union[Any, PredictionForecastResponse]]
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

) -> Optional[Union[Any, PredictionForecastResponse]]:
    """Gets the forecast produced by a prediction

     Obtains the forecast information for the specified prediction if available

    Args:
        id (int):

    Returns:
        Response[Union[Any, PredictionForecastResponse]]
    """


    return (await asyncio_detailed(
        id=id,
client=client,

    )).parsed
