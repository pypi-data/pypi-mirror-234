from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.subscription_event_list import SubscriptionEventList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    subscription_id: str,
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 100,
    status: Union[Unset, None, str] = UNSET,
    resource_id: Union[Unset, None, str] = UNSET,
    authorization: str,
) -> Dict[str, Any]:
    url = "{}/api/v1/hooks/subscriptions/{subscription_id}/events/".format(
        client.base_url, subscription_id=subscription_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    headers["Authorization"] = authorization

    params: Dict[str, Any] = {}
    params["offset"] = offset

    params["limit"] = limit

    params["status"] = status

    params["resource_id"] = resource_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[SubscriptionEventList]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SubscriptionEventList.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[SubscriptionEventList]:
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
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 100,
    status: Union[Unset, None, str] = UNSET,
    resource_id: Union[Unset, None, str] = UNSET,
    authorization: str,
) -> Response[SubscriptionEventList]:
    """Get subscription events

     Get all of the events that have triggered for the given subscription.

    Args:
        subscription_id (str):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 100.
        status (Union[Unset, None, str]):
        resource_id (Union[Unset, None, str]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubscriptionEventList]
    """

    kwargs = _get_kwargs(
        subscription_id=subscription_id,
        client=client,
        offset=offset,
        limit=limit,
        status=status,
        resource_id=resource_id,
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
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 100,
    status: Union[Unset, None, str] = UNSET,
    resource_id: Union[Unset, None, str] = UNSET,
    authorization: str,
) -> Optional[SubscriptionEventList]:
    """Get subscription events

     Get all of the events that have triggered for the given subscription.

    Args:
        subscription_id (str):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 100.
        status (Union[Unset, None, str]):
        resource_id (Union[Unset, None, str]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubscriptionEventList
    """

    return sync_detailed(
        subscription_id=subscription_id,
        client=client,
        offset=offset,
        limit=limit,
        status=status,
        resource_id=resource_id,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    subscription_id: str,
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 100,
    status: Union[Unset, None, str] = UNSET,
    resource_id: Union[Unset, None, str] = UNSET,
    authorization: str,
) -> Response[SubscriptionEventList]:
    """Get subscription events

     Get all of the events that have triggered for the given subscription.

    Args:
        subscription_id (str):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 100.
        status (Union[Unset, None, str]):
        resource_id (Union[Unset, None, str]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubscriptionEventList]
    """

    kwargs = _get_kwargs(
        subscription_id=subscription_id,
        client=client,
        offset=offset,
        limit=limit,
        status=status,
        resource_id=resource_id,
        authorization=authorization,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    subscription_id: str,
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 100,
    status: Union[Unset, None, str] = UNSET,
    resource_id: Union[Unset, None, str] = UNSET,
    authorization: str,
) -> Optional[SubscriptionEventList]:
    """Get subscription events

     Get all of the events that have triggered for the given subscription.

    Args:
        subscription_id (str):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 100.
        status (Union[Unset, None, str]):
        resource_id (Union[Unset, None, str]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubscriptionEventList
    """

    return (
        await asyncio_detailed(
            subscription_id=subscription_id,
            client=client,
            offset=offset,
            limit=limit,
            status=status,
            resource_id=resource_id,
            authorization=authorization,
        )
    ).parsed
