from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.subscription_detail import SubscriptionDetail
from ...types import Response


def _get_kwargs(
    subscription_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Dict[str, Any]:
    url = "{}/api/v1/hooks/subscriptions/{subscription_id}/".format(client.base_url, subscription_id=subscription_id)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[SubscriptionDetail]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SubscriptionDetail.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[SubscriptionDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    subscription_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Response[SubscriptionDetail]:
    """Retrieve a subscription

     Get a single subscription

    Args:
        subscription_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubscriptionDetail]
    """

    kwargs = _get_kwargs(
        subscription_id=subscription_id,
        client=client,
        authorization=authorization,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    subscription_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Optional[SubscriptionDetail]:
    """Retrieve a subscription

     Get a single subscription

    Args:
        subscription_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubscriptionDetail
    """

    return sync_detailed(
        subscription_id=subscription_id,
        client=client,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    subscription_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Response[SubscriptionDetail]:
    """Retrieve a subscription

     Get a single subscription

    Args:
        subscription_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubscriptionDetail]
    """

    kwargs = _get_kwargs(
        subscription_id=subscription_id,
        client=client,
        authorization=authorization,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    subscription_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Optional[SubscriptionDetail]:
    """Retrieve a subscription

     Get a single subscription

    Args:
        subscription_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubscriptionDetail
    """

    return (
        await asyncio_detailed(
            subscription_id=subscription_id,
            client=client,
            authorization=authorization,
        )
    ).parsed
