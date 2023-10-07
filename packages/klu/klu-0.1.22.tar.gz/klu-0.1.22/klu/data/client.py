# mypy: disable-error-code="override"
from typing import Optional

from klu.common.client import KluClientBase
from klu.data.constants import DATA_ENDPOINT
from klu.data.models import Data, DataSourceType
from klu.utils.dict_helpers import dict_no_empty


class DataClient(KluClientBase):
    def __init__(self, api_key: str):
        super().__init__(api_key, DATA_ENDPOINT, Data)

    async def create(
        self,
        input: str,
        output: str,
        action_guid: str,
        full_prompt_sent: Optional[str] = None,
        meta_data: Optional[dict] = None,
        session_guid: Optional[str] = None,
        model: Optional[str] = None,
        model_provider: Optional[str] = None,
        system_message: Optional[str] = None,
        latency: Optional[int] = None,
        num_output_tokens: Optional[int] = None,
        num_input_tokens: Optional[int] = None,
    ) -> Data:
        """
        Creates new data instance for an action_id provided.

        Args:
            issue (str): Data issue
            input (str): Input value of action execution
            output (str): The result of action execution
            rating (int): Data rating
            action_guid (str): Guid of an action data belongs to
            full_prompt_sent (str): String of a full prompt.
            session_guid (str): Guid of a session data belongs to
            meta_data (dict): Data meta_data
            correction (str): Data correction

        Returns:
            Created Data object
        """
        meta_data = meta_data or {}
        return await super().create(
            input=input,
            output=output,
            action=action_guid,
            session=session_guid,
            full_prompt_sent=full_prompt_sent,
            model=model,
            model_provider=model_provider,
            system_message=system_message,
            latency=latency,
            num_output_tokens=num_output_tokens,
            num_input_tokens=num_input_tokens,
            meta_data={
                **meta_data,
                "source": meta_data.pop("source", DataSourceType.SDK),
            },
        )

    async def get(self, guid: str) -> Data:
        """
        Retrieves data information based on the data ID.

        Args:
            guid (str): ID of a datum object to fetch.

        Returns:
            An object
        """
        return await super().get(guid)

    async def update(
        self,
        guid: str,
        meta_data: Optional[dict] = None,
        full_prompt_sent: Optional[str] = None,
        num_output_tokens: Optional[int] = None,
        num_input_tokens: Optional[int] = None,
        latency: Optional[int] = None,
    ) -> Data:
        """
        Updated data information based on the data ID and provided payload. Currently, only supports `output` update.

        Args:

        Returns:
            Newly updated Data object
        """
        data = {
            "meta_data": meta_data,
            "full_prompt_sent": full_prompt_sent,
            "num_output_tokens": num_output_tokens,
            "num_input_tokens": num_input_tokens,
            "latency": latency,
        }
        return await super().update(**{"guid": guid, **dict_no_empty(data)})

    async def delete(self, guid: str) -> Data:
        return await super().delete(guid)
