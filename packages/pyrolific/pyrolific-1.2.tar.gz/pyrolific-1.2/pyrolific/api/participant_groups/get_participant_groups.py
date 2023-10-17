from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_participant_groups_active import GetParticipantGroupsActive
from ...models.participant_group_list_response import ParticipantGroupListResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    active: Union[Unset, None, GetParticipantGroupsActive] = UNSET,
    project_id: str,
) -> Dict[str, Any]:
    url = "{}/api/v1/participant-groups/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_active: Union[Unset, None, str] = UNSET
    if not isinstance(active, Unset):
        json_active = active.value if active else None

    params["active"] = json_active

    params["project_id"] = project_id

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[ParticipantGroupListResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ParticipantGroupListResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[ParticipantGroupListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    active: Union[Unset, None, GetParticipantGroupsActive] = UNSET,
    project_id: str,
) -> Response[ParticipantGroupListResponse]:
    """Get a list of all participant groups within a project

    Args:
        active (Union[Unset, None, GetParticipantGroupsActive]):
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ParticipantGroupListResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        active=active,
        project_id=project_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    active: Union[Unset, None, GetParticipantGroupsActive] = UNSET,
    project_id: str,
) -> Optional[ParticipantGroupListResponse]:
    """Get a list of all participant groups within a project

    Args:
        active (Union[Unset, None, GetParticipantGroupsActive]):
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ParticipantGroupListResponse
    """

    return sync_detailed(
        client=client,
        active=active,
        project_id=project_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    active: Union[Unset, None, GetParticipantGroupsActive] = UNSET,
    project_id: str,
) -> Response[ParticipantGroupListResponse]:
    """Get a list of all participant groups within a project

    Args:
        active (Union[Unset, None, GetParticipantGroupsActive]):
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ParticipantGroupListResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        active=active,
        project_id=project_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    active: Union[Unset, None, GetParticipantGroupsActive] = UNSET,
    project_id: str,
) -> Optional[ParticipantGroupListResponse]:
    """Get a list of all participant groups within a project

    Args:
        active (Union[Unset, None, GetParticipantGroupsActive]):
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ParticipantGroupListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            active=active,
            project_id=project_id,
        )
    ).parsed
