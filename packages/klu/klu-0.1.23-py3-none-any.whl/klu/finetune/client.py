# mypy: disable-error-code="override"
from typing import NoReturn, Optional

import aiohttp
from aiohttp import ClientResponseError

from klu.common.client import KluClientBase
from klu.common.errors import (
    InvalidUpdateParamsError,
    NotSupportedError,
    UnknownKluAPIError,
    UnknownKluError,
)
from klu.finetune.constants import (
    FINE_TUNES_ENDPOINT,
    PROCESS_FINE_TUNE_ENDPOINT,
    READ_FINE_TUNE_STATUS_ENDPOINT,
)
from klu.finetune.errors import FineTuneNotFoundError
from klu.finetune.models import FineTune, FineTuneStatusResponse
from klu.utils.dict_helpers import dict_no_empty


class FineTunesClient(KluClientBase):
    def __init__(self, api_key: str):
        super().__init__(api_key, FINE_TUNES_ENDPOINT, FineTune)

    async def create(self) -> NoReturn:
        raise NotSupportedError()

    async def get(self, guid: str) -> FineTune:
        """
        Retrieves fine_tune information based on the unique FineTune guid, created during the FineTune creation.

        Args:
            guid (str): GUID of a fine_tune to fetch. The one that was used during the fine_tune creation

        Returns:
            FineTune object
        """
        return await super().get(guid)

    async def update(
        self,
        guid: str,
        name: Optional[str] = None,
        openai_fine_tune_name: Optional[str] = None,
    ) -> FineTune:
        """
        Update fine_tune data. At least one of the params has to be provided

        Args:
            guid (str): GUID of a fine_tune to update.
            name: Optional[str]. New fine_tune name
            openai_fine_tune_name: Optional[str]. New fine_tune openai_name

        Returns:
            Updated fine_tune instance
        """

        if not name and not openai_fine_tune_name:
            raise InvalidUpdateParamsError()

        return await super().update(
            **{
                "guid": guid,
                **dict_no_empty(
                    {
                        "name": name,
                        "openai_finetune_name": openai_fine_tune_name,
                    }
                ),
            }
        )

    async def delete(self, guid: str) -> FineTune:
        """
        Delete fine_tune based on the id.

        Args:
            guid (str): Unique Guid of a fine_tune to delete.

        Returns:
            Deleted fine_tune object
        """
        return await super().delete(guid)

    async def process(
        self,
        fine_tune_guid: str,
        base_model: str,
    ) -> FineTune:
        """
        Process the fine_tune.

        Args:
            fine_tune_guid (str): The GUID of the fine_tune to process.
            base_model (str): Can be one of [ada, babbage, curie, davinci] or a fine-tuned model created by your organization.

        Returns:
            The FineTune object
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)

            try:
                response = await client.post(
                    PROCESS_FINE_TUNE_ENDPOINT,
                    {
                        "baseModel": base_model,
                        "finetuneGuid": fine_tune_guid,
                    },
                )
                return FineTune._from_engine_format(response)
            except ClientResponseError as e:
                if e.status == 404:
                    raise FineTuneNotFoundError(fine_tune_guid)

                raise UnknownKluAPIError(e.status, e.message)
            except Exception as e:
                raise UnknownKluError(e)

    async def read_status(
        self,
        fine_tune_guid: str,
    ) -> FineTuneStatusResponse:
        """
        Read fine_tune status.

        Args:
            fine_tune_guid (str): The GUID of the fine_tune to process.

        Returns:
            The status of a FineTune and OpenAI FineTune name
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)

            try:
                response = await client.get(
                    READ_FINE_TUNE_STATUS_ENDPOINT.format(id=fine_tune_guid)
                )
                return FineTuneStatusResponse._create_instance(**response)
            except ClientResponseError as e:
                if e.status == 404:
                    raise FineTuneNotFoundError(fine_tune_guid)

                raise UnknownKluAPIError(e.status, e.message)
            except Exception as e:
                raise UnknownKluError(e)
