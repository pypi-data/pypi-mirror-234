from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.studies_list_response import StudiesListResponse
from ...types import Response


def _get_kwargs(
    project_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Dict[str, Any]:
    url = "{}/api/v1/projects/{project_id}/studies/".format(client.base_url, project_id=project_id)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[StudiesListResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = StudiesListResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[StudiesListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Response[StudiesListResponse]:
    """List all studies in a project

     List all of your studies in a project.

    Args:
        project_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StudiesListResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        client=client,
        authorization=authorization,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Optional[StudiesListResponse]:
    """List all studies in a project

     List all of your studies in a project.

    Args:
        project_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StudiesListResponse
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Response[StudiesListResponse]:
    """List all studies in a project

     List all of your studies in a project.

    Args:
        project_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StudiesListResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        client=client,
        authorization=authorization,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Optional[StudiesListResponse]:
    """List all studies in a project

     List all of your studies in a project.

    Args:
        project_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StudiesListResponse
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            authorization=authorization,
        )
    ).parsed
