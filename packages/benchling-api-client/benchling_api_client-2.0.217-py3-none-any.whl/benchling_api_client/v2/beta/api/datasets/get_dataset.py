from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.dataset import Dataset
from ...models.forbidden_error import ForbiddenError
from ...models.not_found_error import NotFoundError
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    dataset_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/datasets/{dataset_id}".format(client.base_url, dataset_id=dataset_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    params: Dict[str, Any] = {}
    if not isinstance(returning, Unset) and returning is not None:
        params["returning"] = returning

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Dataset, ForbiddenError, NotFoundError]]:
    if response.status_code == 200:
        response_200 = Dataset.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 403:
        response_403 = ForbiddenError.from_dict(response.json(), strict=False)

        return response_403
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Dataset, ForbiddenError, NotFoundError]]:
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
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[Dataset, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        dataset_id=dataset_id,
        returning=returning,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    dataset_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[Dataset, ForbiddenError, NotFoundError]]:
    """Get a dataset and URLs to download its data.

    If the dataset has `SUCCEEDED` status, the `manifest` field in the response will contain URLs to each
    part of a dataset that can be downloaded and the names of the files.

    If the dataset has `NOT_UPLOADED` status, the `manifest` field in the response will contain S3 `PUT` URLs
    to upload dataset `.csv` files. See [Create a dataset](#/Datasets/createDataset) for documentation of
    the full upload flow.

    If the dataset has `FAILED_VALIDATION` or `IN_PROGRESS` status, the `manifest` field in the response will
    only contain the names of the files.

    Note: Manifest URLs are valid for 1 hour after being returned from this endpoint. They should not be stored
    persistently for later use.
    """

    return sync_detailed(
        client=client,
        dataset_id=dataset_id,
        returning=returning,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    dataset_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[Dataset, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        dataset_id=dataset_id,
        returning=returning,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    dataset_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[Dataset, ForbiddenError, NotFoundError]]:
    """Get a dataset and URLs to download its data.

    If the dataset has `SUCCEEDED` status, the `manifest` field in the response will contain URLs to each
    part of a dataset that can be downloaded and the names of the files.

    If the dataset has `NOT_UPLOADED` status, the `manifest` field in the response will contain S3 `PUT` URLs
    to upload dataset `.csv` files. See [Create a dataset](#/Datasets/createDataset) for documentation of
    the full upload flow.

    If the dataset has `FAILED_VALIDATION` or `IN_PROGRESS` status, the `manifest` field in the response will
    only contain the names of the files.

    Note: Manifest URLs are valid for 1 hour after being returned from this endpoint. They should not be stored
    persistently for later use.
    """

    return (
        await asyncio_detailed(
            client=client,
            dataset_id=dataset_id,
            returning=returning,
        )
    ).parsed
