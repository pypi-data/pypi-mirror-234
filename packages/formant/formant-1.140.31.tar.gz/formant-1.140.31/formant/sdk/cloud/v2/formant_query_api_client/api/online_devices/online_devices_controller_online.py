from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.uuid_list_response import UuidListResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    sensitive: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/online-devices".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["sensitive"] = sensitive

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[UuidListResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UuidListResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[UuidListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    sensitive: Union[Unset, None, bool] = UNSET,
) -> Response[UuidListResponse]:
    """Online

     Resource: devices
    Authorized roles: viewer

    Args:
        sensitive (Union[Unset, None, bool]):

    Returns:
        Response[UuidListResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        sensitive=sensitive,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    sensitive: Union[Unset, None, bool] = UNSET,
) -> Optional[UuidListResponse]:
    """Online

     Resource: devices
    Authorized roles: viewer

    Args:
        sensitive (Union[Unset, None, bool]):

    Returns:
        Response[UuidListResponse]
    """

    return sync_detailed(
        client=client,
        sensitive=sensitive,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    sensitive: Union[Unset, None, bool] = UNSET,
) -> Response[UuidListResponse]:
    """Online

     Resource: devices
    Authorized roles: viewer

    Args:
        sensitive (Union[Unset, None, bool]):

    Returns:
        Response[UuidListResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        sensitive=sensitive,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    sensitive: Union[Unset, None, bool] = UNSET,
) -> Optional[UuidListResponse]:
    """Online

     Resource: devices
    Authorized roles: viewer

    Args:
        sensitive (Union[Unset, None, bool]):

    Returns:
        Response[UuidListResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            sensitive=sensitive,
        )
    ).parsed
