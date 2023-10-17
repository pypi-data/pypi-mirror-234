from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.messages import Messages
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Dict[str, Any]:
    url = "{}/api/v1/messages/unread/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    headers["Authorization"] = authorization

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Messages]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Messages.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Messages]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Response[Messages]:
    """Retrieve unread messages

     Get all unread messages.
    The messages you have sent are never returned, only messages you have received and not read.
    It does not mark those messages as read.

    Args:
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Messages]
    """

    kwargs = _get_kwargs(
        client=client,
        authorization=authorization,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Optional[Messages]:
    """Retrieve unread messages

     Get all unread messages.
    The messages you have sent are never returned, only messages you have received and not read.
    It does not mark those messages as read.

    Args:
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Messages
    """

    return sync_detailed(
        client=client,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Response[Messages]:
    """Retrieve unread messages

     Get all unread messages.
    The messages you have sent are never returned, only messages you have received and not read.
    It does not mark those messages as read.

    Args:
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Messages]
    """

    kwargs = _get_kwargs(
        client=client,
        authorization=authorization,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Optional[Messages]:
    """Retrieve unread messages

     Get all unread messages.
    The messages you have sent are never returned, only messages you have received and not read.
    It does not mark those messages as read.

    Args:
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Messages
    """

    return (
        await asyncio_detailed(
            client=client,
            authorization=authorization,
        )
    ).parsed
