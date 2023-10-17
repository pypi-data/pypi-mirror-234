from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.participant_group_membership_list_response import ParticipantGroupMembershipListResponse
from ...models.participant_id_list import ParticipantIDList
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: ParticipantIDList,
) -> Dict[str, Any]:
    url = "{}/api/v1/participant-groups/{id}/participants/".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[ParticipantGroupMembershipListResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ParticipantGroupMembershipListResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[ParticipantGroupMembershipListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: ParticipantIDList,
) -> Response[ParticipantGroupMembershipListResponse]:
    """Add participants to a participant group

     Append participants to a participant group if they are not already members. If a participant is
    already a member of the group, they will be ignored.

    Args:
        id (str):
        json_body (ParticipantIDList):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ParticipantGroupMembershipListResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: ParticipantIDList,
) -> Optional[ParticipantGroupMembershipListResponse]:
    """Add participants to a participant group

     Append participants to a participant group if they are not already members. If a participant is
    already a member of the group, they will be ignored.

    Args:
        id (str):
        json_body (ParticipantIDList):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ParticipantGroupMembershipListResponse
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: ParticipantIDList,
) -> Response[ParticipantGroupMembershipListResponse]:
    """Add participants to a participant group

     Append participants to a participant group if they are not already members. If a participant is
    already a member of the group, they will be ignored.

    Args:
        id (str):
        json_body (ParticipantIDList):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ParticipantGroupMembershipListResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: ParticipantIDList,
) -> Optional[ParticipantGroupMembershipListResponse]:
    """Add participants to a participant group

     Append participants to a participant group if they are not already members. If a participant is
    already a member of the group, they will be ignored.

    Args:
        id (str):
        json_body (ParticipantIDList):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ParticipantGroupMembershipListResponse
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
