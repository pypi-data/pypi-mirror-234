from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ...client import AuthenticatedClient
from ...models.key_value import KeyValue
from ...types import Response


def _get_kwargs(
    key: str,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/key-value/{key}".format(client.base_url, key=key)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[KeyValue]:
    if response.status_code == HTTPStatus.OK:
        response_200 = KeyValue.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[KeyValue]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    key: str,
    *,
    client: AuthenticatedClient,
) -> Response[KeyValue]:
    """Get item

     Get string value from a given key
    Resource: keyValueStorage
    Authorized roles: viewer

    Args:
        key (str):

    Returns:
        Response[KeyValue]
    """

    kwargs = _get_kwargs(
        key=key,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    key: str,
    *,
    client: AuthenticatedClient,
) -> Optional[KeyValue]:
    """Get item

     Get string value from a given key
    Resource: keyValueStorage
    Authorized roles: viewer

    Args:
        key (str):

    Returns:
        Response[KeyValue]
    """

    return sync_detailed(
        key=key,
        client=client,
    ).parsed


async def asyncio_detailed(
    key: str,
    *,
    client: AuthenticatedClient,
) -> Response[KeyValue]:
    """Get item

     Get string value from a given key
    Resource: keyValueStorage
    Authorized roles: viewer

    Args:
        key (str):

    Returns:
        Response[KeyValue]
    """

    kwargs = _get_kwargs(
        key=key,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    key: str,
    *,
    client: AuthenticatedClient,
) -> Optional[KeyValue]:
    """Get item

     Get string value from a given key
    Resource: keyValueStorage
    Authorized roles: viewer

    Args:
        key (str):

    Returns:
        Response[KeyValue]
    """

    return (
        await asyncio_detailed(
            key=key,
            client=client,
        )
    ).parsed
