from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.login_result import LoginResult
from ...models.respond_to_new_password_required_challenge_request import RespondToNewPasswordRequiredChallengeRequest
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: RespondToNewPasswordRequiredChallengeRequest,
) -> Dict[str, Any]:
    url = "{}/auth/respond-to-new-password-required-challenge".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[LoginResult]:
    if response.status_code == HTTPStatus.OK:
        response_200 = LoginResult.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[LoginResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: RespondToNewPasswordRequiredChallengeRequest,
) -> Response[LoginResult]:
    """Respond to new password required challenge

     Respond to New Password Required Challenge

    Args:
        json_body (RespondToNewPasswordRequiredChallengeRequest):

    Returns:
        Response[LoginResult]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: RespondToNewPasswordRequiredChallengeRequest,
) -> Optional[LoginResult]:
    """Respond to new password required challenge

     Respond to New Password Required Challenge

    Args:
        json_body (RespondToNewPasswordRequiredChallengeRequest):

    Returns:
        Response[LoginResult]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: RespondToNewPasswordRequiredChallengeRequest,
) -> Response[LoginResult]:
    """Respond to new password required challenge

     Respond to New Password Required Challenge

    Args:
        json_body (RespondToNewPasswordRequiredChallengeRequest):

    Returns:
        Response[LoginResult]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: RespondToNewPasswordRequiredChallengeRequest,
) -> Optional[LoginResult]:
    """Respond to new password required challenge

     Respond to New Password Required Challenge

    Args:
        json_body (RespondToNewPasswordRequiredChallengeRequest):

    Returns:
        Response[LoginResult]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
