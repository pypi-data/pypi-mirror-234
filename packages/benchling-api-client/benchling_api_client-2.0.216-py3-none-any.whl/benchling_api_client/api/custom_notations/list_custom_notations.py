from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.custom_notations_paginated_list import CustomNotationsPaginatedList
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/custom-notations".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[CustomNotationsPaginatedList]:
    if response.status_code == 200:
        response_200 = CustomNotationsPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[CustomNotationsPaginatedList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[CustomNotationsPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
) -> Optional[CustomNotationsPaginatedList]:
    """ List all available custom notations for specifying modified nucleotide sequences """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[CustomNotationsPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
) -> Optional[CustomNotationsPaginatedList]:
    """ List all available custom notations for specifying modified nucleotide sequences """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
