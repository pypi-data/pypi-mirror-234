from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.submission import Submission
from ...models.submission_transition import SubmissionTransition
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: SubmissionTransition,
    authorization: str,
) -> Dict[str, Any]:
    url = "{}/api/v1/submissions/{id}/transition/".format(client.base_url, id=id)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Submission]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Submission.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Submission]:
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
    json_body: SubmissionTransition,
    authorization: str,
) -> Response[Submission]:
    """Approve or reject a submission

     Transition a submission to `APPROVED` or `REJECTED`. Once the status is changed, it can not be
    restored to its previous value.

    We __strongly__ recommend that, when giving approval to a submission through the API, you first
    observe the `submission.status.change`
    [event](https://docs.prolific.com/docs/api-docs/public/#tag/Hooks/paths/~1api~1v1~1hooks~1event-
    types~1/get) for a status transition to
    `AWAITING_REVIEW` before making the approval request. Our system is currently unable to process
    approvals before this transition.

    Args:
        id (str):
        authorization (str):
        json_body (SubmissionTransition):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Submission]
    """

    kwargs = _get_kwargs(
        id=id,
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
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: SubmissionTransition,
    authorization: str,
) -> Optional[Submission]:
    """Approve or reject a submission

     Transition a submission to `APPROVED` or `REJECTED`. Once the status is changed, it can not be
    restored to its previous value.

    We __strongly__ recommend that, when giving approval to a submission through the API, you first
    observe the `submission.status.change`
    [event](https://docs.prolific.com/docs/api-docs/public/#tag/Hooks/paths/~1api~1v1~1hooks~1event-
    types~1/get) for a status transition to
    `AWAITING_REVIEW` before making the approval request. Our system is currently unable to process
    approvals before this transition.

    Args:
        id (str):
        authorization (str):
        json_body (SubmissionTransition):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Submission
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: SubmissionTransition,
    authorization: str,
) -> Response[Submission]:
    """Approve or reject a submission

     Transition a submission to `APPROVED` or `REJECTED`. Once the status is changed, it can not be
    restored to its previous value.

    We __strongly__ recommend that, when giving approval to a submission through the API, you first
    observe the `submission.status.change`
    [event](https://docs.prolific.com/docs/api-docs/public/#tag/Hooks/paths/~1api~1v1~1hooks~1event-
    types~1/get) for a status transition to
    `AWAITING_REVIEW` before making the approval request. Our system is currently unable to process
    approvals before this transition.

    Args:
        id (str):
        authorization (str):
        json_body (SubmissionTransition):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Submission]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
        authorization=authorization,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: SubmissionTransition,
    authorization: str,
) -> Optional[Submission]:
    """Approve or reject a submission

     Transition a submission to `APPROVED` or `REJECTED`. Once the status is changed, it can not be
    restored to its previous value.

    We __strongly__ recommend that, when giving approval to a submission through the API, you first
    observe the `submission.status.change`
    [event](https://docs.prolific.com/docs/api-docs/public/#tag/Hooks/paths/~1api~1v1~1hooks~1event-
    types~1/get) for a status transition to
    `AWAITING_REVIEW` before making the approval request. Our system is currently unable to process
    approvals before this transition.

    Args:
        id (str):
        authorization (str):
        json_body (SubmissionTransition):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Submission
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
            authorization=authorization,
        )
    ).parsed
