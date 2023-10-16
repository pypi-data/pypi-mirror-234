from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.async_task_link import AsyncTaskLink
from ...models.bad_request_error import BadRequestError
from ...models.dataset_update import DatasetUpdate
from ...models.forbidden_error import ForbiddenError
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    dataset_id: str,
    json_body: DatasetUpdate,
) -> Dict[str, Any]:
    url = "{}/datasets/{dataset_id}".format(client.base_url, dataset_id=dataset_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[AsyncTaskLink, BadRequestError, ForbiddenError, NotFoundError]]:
    if response.status_code == 202:
        response_202 = AsyncTaskLink.from_dict(response.json(), strict=False)

        return response_202
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    if response.status_code == 403:
        response_403 = ForbiddenError.from_dict(response.json(), strict=False)

        return response_403
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[AsyncTaskLink, BadRequestError, ForbiddenError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    dataset_id: str,
    json_body: DatasetUpdate,
) -> Response[Union[AsyncTaskLink, BadRequestError, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        dataset_id=dataset_id,
        json_body=json_body,
    )

    response = client.httpx_client.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    dataset_id: str,
    json_body: DatasetUpdate,
) -> Optional[Union[AsyncTaskLink, BadRequestError, ForbiddenError, NotFoundError]]:
    """Update a dataset.

    After uploading a `.csv` dataset file to S3, call this endpoint to mark the upload status as `IN_PROGRESS`
    to launch a [long-running task](#/Tasks/getTask) to validate and transform the raw `.csv` file into a
    dataset. Once complete, the dataset's status will either be updated to `SUCCEEDED` or `FAILED_VALIDATION`.

    For more details on how we process and validate datasets, [click here](https://docs.benchling.com/docs/datasets-ingestion-reference).

    See [Create a dataset](#/Datasets/createDataset) for documentation of the full upload flow.
    """

    return sync_detailed(
        client=client,
        dataset_id=dataset_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    dataset_id: str,
    json_body: DatasetUpdate,
) -> Response[Union[AsyncTaskLink, BadRequestError, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        dataset_id=dataset_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    dataset_id: str,
    json_body: DatasetUpdate,
) -> Optional[Union[AsyncTaskLink, BadRequestError, ForbiddenError, NotFoundError]]:
    """Update a dataset.

    After uploading a `.csv` dataset file to S3, call this endpoint to mark the upload status as `IN_PROGRESS`
    to launch a [long-running task](#/Tasks/getTask) to validate and transform the raw `.csv` file into a
    dataset. Once complete, the dataset's status will either be updated to `SUCCEEDED` or `FAILED_VALIDATION`.

    For more details on how we process and validate datasets, [click here](https://docs.benchling.com/docs/datasets-ingestion-reference).

    See [Create a dataset](#/Datasets/createDataset) for documentation of the full upload flow.
    """

    return (
        await asyncio_detailed(
            client=client,
            dataset_id=dataset_id,
            json_body=json_body,
        )
    ).parsed
