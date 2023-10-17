from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.filter_set_list import FilterSetList
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    workspace_id: str,
    authorization: str,
) -> Dict[str, Any]:
    url = "{}/api/v1/filter-sets/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    headers["Authorization"] = authorization

    params: Dict[str, Any] = {}
    params["workspace_id"] = workspace_id

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[FilterSetList]:
    if response.status_code == HTTPStatus.OK:
        response_200 = FilterSetList.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[FilterSetList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    workspace_id: str,
    authorization: str,
) -> Response[FilterSetList]:
    """List all filter sets

     List of all filter sets in the specified workspace.

    Args:
        workspace_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FilterSetList]
    """

    kwargs = _get_kwargs(
        client=client,
        workspace_id=workspace_id,
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
    workspace_id: str,
    authorization: str,
) -> Optional[FilterSetList]:
    """List all filter sets

     List of all filter sets in the specified workspace.

    Args:
        workspace_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FilterSetList
    """

    return sync_detailed(
        client=client,
        workspace_id=workspace_id,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    workspace_id: str,
    authorization: str,
) -> Response[FilterSetList]:
    """List all filter sets

     List of all filter sets in the specified workspace.

    Args:
        workspace_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FilterSetList]
    """

    kwargs = _get_kwargs(
        client=client,
        workspace_id=workspace_id,
        authorization=authorization,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    workspace_id: str,
    authorization: str,
) -> Optional[FilterSetList]:
    """List all filter sets

     List of all filter sets in the specified workspace.

    Args:
        workspace_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FilterSetList
    """

    return (
        await asyncio_detailed(
            client=client,
            workspace_id=workspace_id,
            authorization=authorization,
        )
    ).parsed
