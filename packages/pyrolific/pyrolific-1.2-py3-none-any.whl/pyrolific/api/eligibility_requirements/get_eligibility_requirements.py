from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.requirements_response import RequirementsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    authorization: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/eligibility-requirements/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(authorization, Unset):
        headers["Authorization"] = authorization

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[RequirementsResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RequirementsResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[RequirementsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    authorization: Union[Unset, str] = UNSET,
) -> Response[RequirementsResponse]:
    """Get list of all requirements.

     This endpoint is deprecated - please use [Filters](https://docs.prolific.com/docs/api-
    docs/public/#tag/Filters) instead.

    Get a list of all the requirements defined by Prolific that can
    be used to filter participants.

    Args:
        authorization (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RequirementsResponse]
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
    authorization: Union[Unset, str] = UNSET,
) -> Optional[RequirementsResponse]:
    """Get list of all requirements.

     This endpoint is deprecated - please use [Filters](https://docs.prolific.com/docs/api-
    docs/public/#tag/Filters) instead.

    Get a list of all the requirements defined by Prolific that can
    be used to filter participants.

    Args:
        authorization (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RequirementsResponse
    """

    return sync_detailed(
        client=client,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    authorization: Union[Unset, str] = UNSET,
) -> Response[RequirementsResponse]:
    """Get list of all requirements.

     This endpoint is deprecated - please use [Filters](https://docs.prolific.com/docs/api-
    docs/public/#tag/Filters) instead.

    Get a list of all the requirements defined by Prolific that can
    be used to filter participants.

    Args:
        authorization (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RequirementsResponse]
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
    authorization: Union[Unset, str] = UNSET,
) -> Optional[RequirementsResponse]:
    """Get list of all requirements.

     This endpoint is deprecated - please use [Filters](https://docs.prolific.com/docs/api-
    docs/public/#tag/Filters) instead.

    Get a list of all the requirements defined by Prolific that can
    be used to filter participants.

    Args:
        authorization (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RequirementsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            authorization=authorization,
        )
    ).parsed
