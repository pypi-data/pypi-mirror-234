from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_filter_set import CreateFilterSet
from ...models.create_filter_set_response_201 import CreateFilterSetResponse201
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: CreateFilterSet,
    authorization: str,
) -> Dict[str, Any]:
    url = "{}/api/v1/filter-sets/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    headers["Authorization"] = authorization

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[CreateFilterSetResponse201]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = CreateFilterSetResponse201.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[CreateFilterSetResponse201]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: CreateFilterSet,
    authorization: str,
) -> Response[CreateFilterSetResponse201]:
    """Create filter set

     Create a filter set from a list of filters

    Args:
        authorization (str):
        json_body (CreateFilterSet):  Example: [{'workspace_id': '644aaabfaf6bbc363b9d47c6',
            'name': 'Ambidextrous teenagers', 'filters': [{'id': 'handedness', 'selected_values':
            ['2']}, {'id': 'age', 'selected_range': {'lower': 18, 'upper': 19}}]}].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateFilterSetResponse201]
    """

    kwargs = _get_kwargs(
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
    *,
    client: AuthenticatedClient,
    json_body: CreateFilterSet,
    authorization: str,
) -> Optional[CreateFilterSetResponse201]:
    """Create filter set

     Create a filter set from a list of filters

    Args:
        authorization (str):
        json_body (CreateFilterSet):  Example: [{'workspace_id': '644aaabfaf6bbc363b9d47c6',
            'name': 'Ambidextrous teenagers', 'filters': [{'id': 'handedness', 'selected_values':
            ['2']}, {'id': 'age', 'selected_range': {'lower': 18, 'upper': 19}}]}].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateFilterSetResponse201
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: CreateFilterSet,
    authorization: str,
) -> Response[CreateFilterSetResponse201]:
    """Create filter set

     Create a filter set from a list of filters

    Args:
        authorization (str):
        json_body (CreateFilterSet):  Example: [{'workspace_id': '644aaabfaf6bbc363b9d47c6',
            'name': 'Ambidextrous teenagers', 'filters': [{'id': 'handedness', 'selected_values':
            ['2']}, {'id': 'age', 'selected_range': {'lower': 18, 'upper': 19}}]}].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateFilterSetResponse201]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        authorization=authorization,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: CreateFilterSet,
    authorization: str,
) -> Optional[CreateFilterSetResponse201]:
    """Create filter set

     Create a filter set from a list of filters

    Args:
        authorization (str):
        json_body (CreateFilterSet):  Example: [{'workspace_id': '644aaabfaf6bbc363b9d47c6',
            'name': 'Ambidextrous teenagers', 'filters': [{'id': 'handedness', 'selected_values':
            ['2']}, {'id': 'age', 'selected_range': {'lower': 18, 'upper': 19}}]}].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateFilterSetResponse201
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            authorization=authorization,
        )
    ).parsed
