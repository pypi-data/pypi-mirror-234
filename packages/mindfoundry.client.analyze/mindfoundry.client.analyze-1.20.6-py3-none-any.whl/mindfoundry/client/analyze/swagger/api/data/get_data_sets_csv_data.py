from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: int,
    *,
    client: Client,
    separator: Union[Unset, None, str] = UNSET,
    quote_char: Union[Unset, None, str] = UNSET,
    escape_char: Union[Unset, None, str] = UNSET,
    charset: Union[Unset, None, str] = 'UTF-8',

) -> Dict[str, Any]:
    url = "{}/v1/dataSets/{id}/data/csv".format(
        client.base_url,id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    params: Dict[str, Any] = {}
    params["separator"] = separator


    params["quoteChar"] = quote_char


    params["escapeChar"] = escape_char


    params["charset"] = charset



    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    

    

    return {
	    "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }




def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    id: int,
    *,
    client: Client,
    separator: Union[Unset, None, str] = UNSET,
    quote_char: Union[Unset, None, str] = UNSET,
    escape_char: Union[Unset, None, str] = UNSET,
    charset: Union[Unset, None, str] = 'UTF-8',

) -> Response[Any]:
    """Get the data in CSV format

     Get the data from the latest version of the data set as a csv file

    Args:
        id (int):
        separator (Union[Unset, None, str]):
        quote_char (Union[Unset, None, str]):
        escape_char (Union[Unset, None, str]):
        charset (Union[Unset, None, str]):  Default: 'UTF-8'.

    Returns:
        Response[Any]
    """


    kwargs = _get_kwargs(
        id=id,
client=client,
separator=separator,
quote_char=quote_char,
escape_char=escape_char,
charset=charset,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    id: int,
    *,
    client: Client,
    separator: Union[Unset, None, str] = UNSET,
    quote_char: Union[Unset, None, str] = UNSET,
    escape_char: Union[Unset, None, str] = UNSET,
    charset: Union[Unset, None, str] = 'UTF-8',

) -> Response[Any]:
    """Get the data in CSV format

     Get the data from the latest version of the data set as a csv file

    Args:
        id (int):
        separator (Union[Unset, None, str]):
        quote_char (Union[Unset, None, str]):
        escape_char (Union[Unset, None, str]):
        charset (Union[Unset, None, str]):  Default: 'UTF-8'.

    Returns:
        Response[Any]
    """


    kwargs = _get_kwargs(
        id=id,
client=client,
separator=separator,
quote_char=quote_char,
escape_char=escape_char,
charset=charset,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

