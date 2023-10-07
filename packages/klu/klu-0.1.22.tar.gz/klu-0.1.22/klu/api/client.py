from functools import wraps
from typing import List, Optional, Union

import aiohttp
from aiohttp import ClientResponseError

from klu.api.config import get_api_url
from klu.common.errors import (
    BadRequestAPIError,
    InvalidApiMethodUsedError,
    InvalidDataSent,
    UnauthorizedError,
    UnknownKluAPIError,
    UnknownKluError,
)


def _handle_http_exception(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ClientResponseError as e:
            if e.status == 400:
                raise BadRequestAPIError(e.status, e.message)
            if e.status == 500:
                raise UnknownKluAPIError(e.status, e.message)
            if e.status == 401:
                raise UnauthorizedError()
            if e.status == 405:
                raise InvalidApiMethodUsedError(e.status, e.message)
            if e.status == 422:
                raise InvalidDataSent(e.status, e.message)

            # Passing higher for more specific handling up to the functions level.
            raise e
        except Exception as e:
            raise UnknownKluError(e)

    return wrapper


class APIClient:
    def __init__(self, session: aiohttp.ClientSession, api_key: str):
        self.session = session
        self.api_url = get_api_url()
        self.headers = {"Authorization": f"Bearer {api_key}"}

    @_handle_http_exception
    async def get(
        self, path: str, params: Optional[dict] = None, api_url: Optional[str] = None
    ) -> Union[dict, List[dict]]:
        url = f"{self.api_url if api_url is None else api_url}{path}"
        async with self.session.get(
            url, params=params, headers=self.headers
        ) as response:
            response.raise_for_status()
            return await response.json()

    @_handle_http_exception
    async def post(self, path: str, json_data: Optional[dict] = None) -> dict:
        url = f"{self.api_url}{path}"
        async with self.session.post(
            url, json=json_data, headers=self.headers
        ) as response:
            if not response.ok and response.content_type == "application/json":
                content = await response.json()
                detail_message = content.get("detail") if content else None

                if detail_message:
                    response.reason = detail_message

            response.raise_for_status()
            return await response.json()

    @_handle_http_exception
    async def put(self, path: str, json_data: dict) -> dict:
        url = f"{self.api_url}{path}"
        async with self.session.put(
            url, json=json_data, headers=self.headers
        ) as response:
            response.raise_for_status()
            return await response.json()

    @_handle_http_exception
    async def delete(self, path: str) -> dict:
        url = f"{self.api_url}{path}"
        async with self.session.delete(url, headers=self.headers) as response:
            response.raise_for_status()
            return await response.json()
