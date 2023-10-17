from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.project import Project
from ...types import Response


def _get_kwargs(
    project_id: str,
    *,
    client: AuthenticatedClient,
    json_body: Project,
    authorization: str,
) -> Dict[str, Any]:
    url = "{}/api/v1/projects/{project_id}/".format(client.base_url, project_id=project_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    headers["Authorization"] = authorization

    json_json_body = json_body.to_dict()

    return {
        "method": "patch",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Project]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Project.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Project]:
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
    json_body: Project,
    authorization: str,
) -> Response[Project]:
    """Update a project

     Update a project's details

    Args:
        project_id (str):
        authorization (str):
        json_body (Project):  Example: {'id': '62fce6fff0a78eb4f3ebc09c', 'title': 'My project',
            'description': 'This project is for...', 'owner': '60a42f4c693c29420793cb73', 'users':
            [{'id': '60a42f4c693c29420793cb73', 'name': 'Joe Soap', 'email': 'joe.soap@gmail.com',
            'roles': ['PROJECT_EDITOR']}], 'workspace': '60a42f4c693c29420793cb73',
            'naivety_distribution_rate': 0.5}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Project]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        client=client,
        json_body=json_body,
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
    json_body: Project,
    authorization: str,
) -> Optional[Project]:
    """Update a project

     Update a project's details

    Args:
        project_id (str):
        authorization (str):
        json_body (Project):  Example: {'id': '62fce6fff0a78eb4f3ebc09c', 'title': 'My project',
            'description': 'This project is for...', 'owner': '60a42f4c693c29420793cb73', 'users':
            [{'id': '60a42f4c693c29420793cb73', 'name': 'Joe Soap', 'email': 'joe.soap@gmail.com',
            'roles': ['PROJECT_EDITOR']}], 'workspace': '60a42f4c693c29420793cb73',
            'naivety_distribution_rate': 0.5}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Project
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        json_body=json_body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    json_body: Project,
    authorization: str,
) -> Response[Project]:
    """Update a project

     Update a project's details

    Args:
        project_id (str):
        authorization (str):
        json_body (Project):  Example: {'id': '62fce6fff0a78eb4f3ebc09c', 'title': 'My project',
            'description': 'This project is for...', 'owner': '60a42f4c693c29420793cb73', 'users':
            [{'id': '60a42f4c693c29420793cb73', 'name': 'Joe Soap', 'email': 'joe.soap@gmail.com',
            'roles': ['PROJECT_EDITOR']}], 'workspace': '60a42f4c693c29420793cb73',
            'naivety_distribution_rate': 0.5}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Project]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        client=client,
        json_body=json_body,
        authorization=authorization,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    json_body: Project,
    authorization: str,
) -> Optional[Project]:
    """Update a project

     Update a project's details

    Args:
        project_id (str):
        authorization (str):
        json_body (Project):  Example: {'id': '62fce6fff0a78eb4f3ebc09c', 'title': 'My project',
            'description': 'This project is for...', 'owner': '60a42f4c693c29420793cb73', 'users':
            [{'id': '60a42f4c693c29420793cb73', 'name': 'Joe Soap', 'email': 'joe.soap@gmail.com',
            'roles': ['PROJECT_EDITOR']}], 'workspace': '60a42f4c693c29420793cb73',
            'naivety_distribution_rate': 0.5}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Project
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            json_body=json_body,
            authorization=authorization,
        )
    ).parsed
