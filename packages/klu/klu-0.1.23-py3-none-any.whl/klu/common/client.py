from abc import abstractmethod
from typing import Type, TypeVar

import aiohttp
from aiohttp import ClientResponseError

from klu.api.client import APIClient
from klu.common.errors import (
    IdNotProvidedError,
    InstanceNotFoundError,
    InstanceRelationshipNotFoundError,
)
from klu.common.models import BaseEngineModel

T = TypeVar("T", bound=BaseEngineModel)


class KluClientBase:
    def __init__(self, api_key: str, base_path: str, model: Type[T]):
        self._model = model
        self._api_key = api_key
        self._base_path = base_path

    def _get_api_client(self, session):
        return APIClient(session, self._api_key)

    @abstractmethod
    async def create(self, **kwargs) -> T:
        # Some endpoints use a different url for creation
        # TODO ideally, this should be the same. Create a task on the engine side.
        url = kwargs.pop("url", None)
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            try:
                response = await client.post(url or self._base_path, kwargs)
                return self._model._from_engine_format(response)  # type: ignore
            except ClientResponseError as e:
                if e.status == 404:
                    raise InstanceRelationshipNotFoundError(
                        self._model.__name__, e.message
                    )

                raise e

    @abstractmethod
    async def get(self, guid: str) -> T:
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            try:
                response = await client.get(f"{self._base_path}{guid}")
                return self._model._from_engine_format(response)  # type: ignore
            except ClientResponseError as e:
                if e.status == 404:
                    raise InstanceNotFoundError(self._model.__name__, guid)

                raise e

    @abstractmethod
    async def update(self, **kwargs) -> T:
        id = kwargs.pop("guid", None)
        if not id:
            raise IdNotProvidedError()

        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            try:
                response = await client.put(f"{self._base_path}{id}", kwargs)
                return self._model._from_engine_format(response)  # type: ignore
            except ClientResponseError as e:
                if e.status == 404:
                    raise InstanceNotFoundError(self._model.__name__, id)

                raise e

    @abstractmethod
    async def delete(self, guid: str) -> T:
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            try:
                response = await client.delete(f"{self._base_path}{guid}")
                return self._model._from_engine_format(response)  # type: ignore
            except ClientResponseError as e:
                if e.status == 404:
                    raise InstanceNotFoundError(self._model.__name__, guid)

                raise e
