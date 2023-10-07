# mypy: disable-error-code="override"
from typing import List, Optional

import aiohttp
from aiohttp import ClientResponseError

from klu.common.client import KluClientBase
from klu.common.errors import InvalidUpdateParamsError, UnknownKluAPIError
from klu.model.constants import (
    MODEL_ENDPOINT,
    PROVIDERS_ENDPOINT,
    VALIDATE_MODEL_API_KEY_ENDPOINT,
)
from klu.model.errors import UnknownModelProviderError
from klu.model.models import Model, Provider, ProviderWithModels
from klu.utils.dict_helpers import dict_no_empty


class ModelsClient(KluClientBase):
    def __init__(self, api_key: str):
        super().__init__(api_key, MODEL_ENDPOINT, Model)

    async def create(
        self,
        llm: str,
        provider: str,
        key: str,
        url: Optional[str] = None,
        default: Optional[bool] = False,
    ) -> Model:
        """
                Creates a model based on the data provided.

                Args:
                    llm (str): Model llm. Required
                    workspace_model_provider_id (str): Unique identifier of model provider.
                        Can be retrieved from a model providers listing endpoint.

                Returns:
        A newly created Model object.
        """
        return await super().create(
            llm=llm, provider=provider, key=key, url=url, default=default
        )

    async def get(self, guid: str) -> Model:
        """
        Retrieves model  information based on the id.

        Args:
            guid (str): GUID of a model to fetch. The one that was used during the model creation

        Returns:
            Model object
        """
        return await super().get(guid)

    async def update(
        self, guid: str, llm: Optional[str] = None, key: Optional[str] = None
    ) -> Model:
        """
        Update model data. At least one of the params has to be provided

        Args:
            guid (str): GUID of a model to update
            llm: Optional[str]. New model
            key: Optional[str]. New model key

        Returns:
            Updated app instance
        """
        if not llm and not key:
            raise InvalidUpdateParamsError()

        return await super().update(
            **{"guid": guid, **dict_no_empty({"llm": llm, "key": key})}
        )

    async def delete(self, guid: str) -> Model:
        """
        Delete model based on the id.

        Args:
            guid (str): ID of a model to delete.

        Returns:
            Deleted model object
        """
        return await super().delete(guid)

    async def validate_key(self, api_key: str, provider: str) -> bool:
        """
        Validates API keys for provided api_key and provider values.

        Args:
            api_key (str): Model api_key
            provider (int): Model provider id. Should be taken from the UI.

        Returns:
            A JSON response with a message about successful creation if model was created.
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            try:
                response = await client.post(
                    VALIDATE_MODEL_API_KEY_ENDPOINT,
                    {
                        "api_key": api_key,
                        "provider": provider,
                    },
                )
                return bool(response.get("validated"))
            except ClientResponseError as e:
                if e.status == 404:
                    raise UnknownModelProviderError(provider)

                raise UnknownKluAPIError(e.status, e.message)

    async def add_provider(
        self,
        provider: str,
        key: str,
        url: Optional[str] = None,
        default: Optional[bool] = False,
    ) -> ProviderWithModels:
        """
                Creates a model based on the data provided.

                Args:
                    llm (str): Model llm. Required
                    workspace_model_provider_id (str): Unique identifier of model provider.
                        Can be retrieved from a model providers listing endpoint.

                Returns:
        A newly created Model object.
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            try:
                response = await client.post(
                    PROVIDERS_ENDPOINT,
                    {
                        "provider": provider,
                        "key": key,
                        "url": url,
                        "default": default,
                    },
                )
                provider = Provider._from_engine_format(response.pop("provider"))  # type: ignore
                models = []
                for model in response["models"]:
                    temp = Model._from_engine_format(model)  # type: ignore
                    models.append(temp)  # type: ignore
                return ProviderWithModels(provider=provider, models=models)  # type: ignore
            except ClientResponseError as e:
                raise UnknownKluAPIError(e.status, e.message)

    async def get_providers(self) -> List[Provider]:
        """
        Retrievel all providers in the workspace

        Returns:
            List of Provider objects
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            try:
                response = await client.get(
                    PROVIDERS_ENDPOINT,
                )
                providers = []
                for provider in response:
                    providers.append(Provider._from_engine_format(provider))  # type: ignore
                return providers  # type: ignore
            except ClientResponseError as e:
                raise UnknownKluAPIError(e.status, e.message)

    async def delete_provider(self, guid: str) -> bool:
        """
        Retrievel all providers in the workspace

        Returns:
            List of Model objects
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            try:
                response = await client.delete(
                    PROVIDERS_ENDPOINT + guid,
                )
                if response == "Success":
                    return True
                else:
                    return False
            except ClientResponseError as e:
                raise UnknownKluAPIError(e.status, e.message)

    async def get_all(self) -> List[Model]:
        """
        Retrievel all models in the workspace

        Returns:
            List of Model objects
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            try:
                response = await client.get(
                    MODEL_ENDPOINT,
                )
                models = []
                for model in response:
                    models.append(Model._from_engine_format(model))
                return models
            except ClientResponseError as e:
                raise UnknownKluAPIError(e.status, e.message)
