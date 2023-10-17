from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.export_study_method import ExportStudyMethod
from ...models.export_study_response_200 import ExportStudyResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: AuthenticatedClient,
    method: Union[Unset, None, ExportStudyMethod] = UNSET,
    authorization: str,
) -> Dict[str, Any]:
    url = "{}/api/v1/studies/{id}/export/".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    headers["Authorization"] = authorization

    params: Dict[str, Any] = {}
    json_method: Union[Unset, None, str] = UNSET
    if not isinstance(method, Unset):
        json_method = method.value if method else None

    params["method"] = json_method

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[ExportStudyResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ExportStudyResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[ExportStudyResponse200]:
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
    method: Union[Unset, None, ExportStudyMethod] = UNSET,
    authorization: str,
) -> Response[ExportStudyResponse200]:
    """Download demographic data

     __This is an evolving feature and the exact content of such exports is subject to change, so use at
    your own risk.__

    Download a snapshot of the participants' prescreening responses at the time that they took your
    study. Specify the optional `?method=EMAIL` query parameter if you want this to be sent to your
    email.

    In addition to the responses to all prescreeners applied to the study (subject to change), you'll
    also have access to the following data:

    * Submission id
    * Participant id
    * Submission status
    * Started date-time
      * Expressed in UTC
      * ISO 8601 formatted
    * Completed date-time
      * Expressed in UTC
      * ISO 8601 formatted
    * Time taken (in seconds)
    * Age
    * Sex
      * Participants were asked the following question: What is your sex, as recorded on legal/official
    documents?
    * First language
    * Current country of residence
    * Nationality
    * Country of birth
    * Student status
    * Employment status
    * Reviewed at date-time
      * Expressed in UTC
      * ISO 8601 formatted
    * Completion code ('entered code')

    Learn more on [Exporting Prolific demographic data](https://researcher-help.prolific.com/hc/en-
    gb/articles/360009391633-Exporting-Prolific-demographic-data).

    Args:
        id (str):
        method (Union[Unset, None, ExportStudyMethod]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExportStudyResponse200]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        method=method,
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
    method: Union[Unset, None, ExportStudyMethod] = UNSET,
    authorization: str,
) -> Optional[ExportStudyResponse200]:
    """Download demographic data

     __This is an evolving feature and the exact content of such exports is subject to change, so use at
    your own risk.__

    Download a snapshot of the participants' prescreening responses at the time that they took your
    study. Specify the optional `?method=EMAIL` query parameter if you want this to be sent to your
    email.

    In addition to the responses to all prescreeners applied to the study (subject to change), you'll
    also have access to the following data:

    * Submission id
    * Participant id
    * Submission status
    * Started date-time
      * Expressed in UTC
      * ISO 8601 formatted
    * Completed date-time
      * Expressed in UTC
      * ISO 8601 formatted
    * Time taken (in seconds)
    * Age
    * Sex
      * Participants were asked the following question: What is your sex, as recorded on legal/official
    documents?
    * First language
    * Current country of residence
    * Nationality
    * Country of birth
    * Student status
    * Employment status
    * Reviewed at date-time
      * Expressed in UTC
      * ISO 8601 formatted
    * Completion code ('entered code')

    Learn more on [Exporting Prolific demographic data](https://researcher-help.prolific.com/hc/en-
    gb/articles/360009391633-Exporting-Prolific-demographic-data).

    Args:
        id (str):
        method (Union[Unset, None, ExportStudyMethod]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExportStudyResponse200
    """

    return sync_detailed(
        id=id,
        client=client,
        method=method,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    method: Union[Unset, None, ExportStudyMethod] = UNSET,
    authorization: str,
) -> Response[ExportStudyResponse200]:
    """Download demographic data

     __This is an evolving feature and the exact content of such exports is subject to change, so use at
    your own risk.__

    Download a snapshot of the participants' prescreening responses at the time that they took your
    study. Specify the optional `?method=EMAIL` query parameter if you want this to be sent to your
    email.

    In addition to the responses to all prescreeners applied to the study (subject to change), you'll
    also have access to the following data:

    * Submission id
    * Participant id
    * Submission status
    * Started date-time
      * Expressed in UTC
      * ISO 8601 formatted
    * Completed date-time
      * Expressed in UTC
      * ISO 8601 formatted
    * Time taken (in seconds)
    * Age
    * Sex
      * Participants were asked the following question: What is your sex, as recorded on legal/official
    documents?
    * First language
    * Current country of residence
    * Nationality
    * Country of birth
    * Student status
    * Employment status
    * Reviewed at date-time
      * Expressed in UTC
      * ISO 8601 formatted
    * Completion code ('entered code')

    Learn more on [Exporting Prolific demographic data](https://researcher-help.prolific.com/hc/en-
    gb/articles/360009391633-Exporting-Prolific-demographic-data).

    Args:
        id (str):
        method (Union[Unset, None, ExportStudyMethod]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExportStudyResponse200]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        method=method,
        authorization=authorization,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    method: Union[Unset, None, ExportStudyMethod] = UNSET,
    authorization: str,
) -> Optional[ExportStudyResponse200]:
    """Download demographic data

     __This is an evolving feature and the exact content of such exports is subject to change, so use at
    your own risk.__

    Download a snapshot of the participants' prescreening responses at the time that they took your
    study. Specify the optional `?method=EMAIL` query parameter if you want this to be sent to your
    email.

    In addition to the responses to all prescreeners applied to the study (subject to change), you'll
    also have access to the following data:

    * Submission id
    * Participant id
    * Submission status
    * Started date-time
      * Expressed in UTC
      * ISO 8601 formatted
    * Completed date-time
      * Expressed in UTC
      * ISO 8601 formatted
    * Time taken (in seconds)
    * Age
    * Sex
      * Participants were asked the following question: What is your sex, as recorded on legal/official
    documents?
    * First language
    * Current country of residence
    * Nationality
    * Country of birth
    * Student status
    * Employment status
    * Reviewed at date-time
      * Expressed in UTC
      * ISO 8601 formatted
    * Completion code ('entered code')

    Learn more on [Exporting Prolific demographic data](https://researcher-help.prolific.com/hc/en-
    gb/articles/360009391633-Exporting-Prolific-demographic-data).

    Args:
        id (str):
        method (Union[Unset, None, ExportStudyMethod]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExportStudyResponse200
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            method=method,
            authorization=authorization,
        )
    ).parsed
