# mypy: disable-error-code="override"
from typing import List, Optional

import aiohttp
from aiohttp import ClientResponseError

from klu.action.constants import (
    ACTION_DATA_ENDPOINT,
    ACTION_ENDPOINT,
    CREATE_ACTION_ENDPOINT,
    DEFAULT_ACTIONS_PAGE_SIZE,
    PLAYGROUND_PROMPT_ENDPOINT,
)
from klu.action.errors import ActionNotFoundError, InvalidActionPromptData
from klu.action.models import (
    Action,
    AsyncPromptResponse,
    AsyncPromptResultResponse,
    PromptResponse,
    StreamingPromptResponse,
    SyncPromptResponse,
)
from klu.common.client import KluClientBase
from klu.common.errors import (
    InvalidUpdateParamsError,
    UnknownKluAPIError,
    UnknownKluError,
)
from klu.common.models import PromptInput
from klu.data.models import Data
from klu.utils.dict_helpers import dict_no_empty
from klu.utils.paginator import Paginator
from klu.workspace.errors import WorkspaceOrUserNotFoundError


class ActionsClient(KluClientBase):
    def __init__(self, api_key: str):
        super().__init__(api_key, ACTION_ENDPOINT, Action)
        self._paginator = Paginator(ACTION_ENDPOINT)

    # type: ignore
    async def create(
        self,
        name: str,
        prompt: str,
        app_guid: str,
        model_guid: str,
        action_type: str,
        description: str,
        system_message: Optional[str] = None,
        model_config: Optional[dict] = None,
    ) -> Action:
        """
        Creates new action instance

        Args:
            name (str): Action name
            prompt (str): Action prompt
            model_guid (int): Guid of a model used for action
            app_guid (str): GUID of the app for an action to be attached to
            action_type (str): The type of the action. Can be one of ['prompt', 'chat', 'workflow', 'worker', 'type']
            description (str): The description of the action
            model_config (str): Optional action model configuration dict

        Returns:
            Newly created Action object
        """
        return await super().create(
            name=name,
            prompt=prompt,
            app_guid=app_guid,
            model_guid=model_guid,
            action_type=action_type,
            description=description,
            model_config=model_config,
            system_message=system_message,
            url=CREATE_ACTION_ENDPOINT,
        )

    # type: ignore
    async def get(self, guid: str) -> Action:
        """
        Get an action defined by the id

        Args:
            guid (str): The id of an action to retrieve

        Returns:
            Retrieved Action object.
        """
        return await super().get(guid)

    # type: ignore
    async def update(
        self,
        guid: str,
        name: Optional[str] = None,
        prompt: Optional[str] = None,
        description: Optional[str] = None,
        model_config: Optional[str] = None,
        system_message: Optional[str] = None,
    ) -> Action:
        """
        Update action instance with provided data. At least one of parameters should be present.

        Args:
            guid (str): The GUID of the action to update.
            name: Optional[str]. New action name.
            prompt: Optional[str]. New action type.
            description: Optional[str]. New action description.
            model_config: Optional[dict]. New action model_config.

        Returns:
            Action with updated data
        """
        if not name and not prompt and not description and not model_config:
            raise InvalidUpdateParamsError()

        return await super().update(
            **{
                "guid": guid,
                **dict_no_empty(
                    {
                        "name": name,
                        "prompt": prompt,
                        "description": description,
                        "model_config": model_config,
                        "system_message": system_message,
                    }
                ),
            }
        )

    async def delete(self, guid: str) -> Action:
        """
        Delete an action defined by the id

        Args:
            guid (str): The id of an action to delete

        Returns:
            Deleted Action object.
        """
        return await super().delete(guid)

    async def prompt(
        self,
        action: str,
        input: PromptInput,
        filter: Optional[str] = None,
        session: Optional[str] = None,
        metadata_filter: Optional[dict] = None,
    ) -> SyncPromptResponse:
        """
        Run a prompt with an agent, optionally using streaming.

        Args:
            action (str): The GUID of the agent to run the prompt with.
            input (PromptInput): The prompt to run with the agent.
            filter (Optional[str]): The filter to use when running the prompt.
            session (Optional[str]): The GUID of the session to run the prompt with.

        Returns:
            An object result of running the prompt with the message and a feedback_url for providing feedback.
        """
        response = await self._run_prompt(
            action=action,
            input=input,
            filter=filter,
            streaming=False,
            async_mode=False,
            session=session,
            metadata_filter=metadata_filter,
        )
        return SyncPromptResponse._create_instance(**response.__dict__)

    async def async_prompt(
        self,
        action: str,
        input: PromptInput,
        filter: Optional[str] = None,
        session: Optional[str] = None,
    ) -> AsyncPromptResponse:
        """
        Run a prompt with an agent, optionally using streaming.

        Args:
            action (str): The GUID of the agent to run the prompt with.
            input (PromptInput): The prompt to run with the agent.
            filter (Optional[str]): The filter to use when running the prompt.
            session (Optional[str]): The GUID of the session to run the prompt with.

        Returns:
            An object result of running the prompt with the message and a feedback_url for providing feedback.
            Also contains result_url - the url that gives access to the result when the prompt is completed or a message about prompting in progress.
        """
        response = await self._run_prompt(
            action=action,
            input=input,
            filter=filter,
            streaming=False,
            async_mode=True,
            session=session,
        )
        return AsyncPromptResponse._create_instance(**response.__dict__)

    async def get_async_prompt_result(
        self,
        result_url: str,
    ) -> AsyncPromptResultResponse:
        """
        Get a result of async prompting

        Args:
            result_url (str): The url you received in response to calling async_prompt function

        Returns:
            An object with the message, which contains either prompt result or a message about prompt still being in progress.
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)

            response = await client.get(result_url, api_url="")
            return AsyncPromptResultResponse._create_instance(**response)

    async def stream(
        self,
        action: str,
        input: PromptInput,
        filter: Optional[str] = None,
        session: Optional[str] = None,
    ) -> StreamingPromptResponse:
        """
        Run a prompt with an agent, optionally using streaming.

        Args:
            action (str): The GUID of the agent to run the prompt with.
            input (PromptInput): The prompt to run with the agent.
            filter (Optional[str]): The filter to use when running the prompt.
            session (Optional[str]): The GUID of the session to run the prompt with.

        Returns:
            An object result of running the prompt with the message, feedback_url for providing feedback.
            The response will also contain data stream, which can be used to consume the prompt response message
        """
        prompt_response = await self._run_prompt(
            action,
            input=input,
            filter=filter,
            streaming=True,
            async_mode=False,
            session=session,
        )

        return StreamingPromptResponse._create_instance(**prompt_response.__dict__)

    async def _run_prompt(
        self,
        action: str,
        input: PromptInput,
        filter: Optional[str] = None,
        streaming: Optional[bool] = False,
        async_mode: Optional[bool] = False,
        session: Optional[str] = None,
        metadata_filter: Optional[dict] = None,
    ) -> PromptResponse:
        async with aiohttp.ClientSession() as _session:
            client = self._get_api_client(_session)

            try:
                response = await client.post(
                    ACTION_ENDPOINT,
                    {
                        "input": input,
                        "filter": filter,
                        "action": action,
                        "streaming": streaming,
                        "async_mode": async_mode,
                        "session": session,
                        "metadata_filter": metadata_filter,
                    },
                )
                return PromptResponse(**response)
            except ClientResponseError as e:
                if e.status == 404:
                    raise ActionNotFoundError(action)

                raise UnknownKluAPIError(e.status, e.message)
            except Exception as e:
                raise UnknownKluError(e)

    async def playground(
        self,
        prompt: str,
        model_id: int,
        values: Optional[dict] = None,
        tool_ids: Optional[list] = None,
        index_ids: Optional[list] = None,
        model_config: Optional[dict] = None,
    ) -> StreamingPromptResponse:
        """
        Run a prompt with an agent. Always uses streaming

        Args:
            prompt (str): The prompt to run.
            model_id (int): The ID of the model to use. Can be retrieved by querying the model by guid
            tool_ids (list): Optional list of tool IDs to use. Defaults to an empty array
            index_ids (list): Optional list of index IDs to use. Defaults to an empty array
            values (Optional[dict]): The values to be interpolated into the prompt template, or appended to the prompt template if it doesn't include variables
            model_config (Optional[dict]): Configuration of the model

        Returns:
            An object result of running the prompt with the message and a feedback_url for providing feedback.
        """
        tool_ids = tool_ids or []
        index_ids = index_ids or []

        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)

            try:
                response = await client.post(
                    PLAYGROUND_PROMPT_ENDPOINT,
                    {
                        "prompt": prompt,
                        "values": values,
                        "toolIds": tool_ids,
                        "modelId": model_id,
                        "indexIds": index_ids,
                        "modelConfig": model_config,
                    },
                )
                return StreamingPromptResponse._create_instance(**response)
            except ClientResponseError as e:
                if e.status == 404:
                    raise WorkspaceOrUserNotFoundError()
                if e.status == 400:
                    raise InvalidActionPromptData(e.message)

                raise UnknownKluAPIError(e.status, e.message)
            except Exception as e:
                raise UnknownKluError(e)

    async def get_data(self, guid: str) -> List[Data]:
        """
        Retrieves data information for an action.

        Args:
            guid (str): Guid of an action to fetch data for.

        Returns:
            An array of actions found by provided app id.
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)

            try:
                response = await client.get(ACTION_DATA_ENDPOINT.format(id=guid))
                return [Data._from_engine_format(data) for data in response]
            except ClientResponseError as e:
                if e.status == 404:
                    raise ActionNotFoundError(guid)

                raise UnknownKluAPIError(e.status, e.message)
            except Exception as e:
                raise UnknownKluError(e)

    async def list(self) -> List[Action]:
        """
        Retrieves all actions for a user represented by the used API_KEY.
        Does not rely on internal paginator state, so `reset_pagination` method call can be skipped

        Returns (List[Action]): An array of all actions
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            response = await self._paginator.fetch_all(client)

            return [Action._from_engine_format(action) for action in response]

    async def fetch_single_page(
        self, page_number, limit: int = DEFAULT_ACTIONS_PAGE_SIZE
    ) -> List[Action]:
        """
        Retrieves a single page of actions.
        Can be used to fetch a specific page of actions provided a certain per_page config.
        Does not rely on internal paginator state, so `reset_pagination` method call can be skipped

        Args:
            page_number (int): Number of the page to fetch
            limit (int): Number of instances to fetch per page. Defaults to 50

        Returns:
            An array of actions fetched for a queried page. Empty if queried page does not exist
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            response = await self._paginator.fetch_single_page(
                client, page_number, limit=limit
            )

            return [Action._from_engine_format(action) for action in response]

    async def fetch_next_page(
        self, limit: int = DEFAULT_ACTIONS_PAGE_SIZE, offset: Optional[int] = None
    ) -> List[Action]:
        """
        Retrieves the next page of actions. Can be used to fetch a flexible number of pages starting.
        The place to start from can be controlled by the offset parameter.
        After using this method, we suggest to call `reset_pagination` method to reset the page cursor.

        Args:
            limit (int): Number of instances to fetch per page. Defaults to 50
            offset (int): The number of instances to skip. Can be used to query the pages of actions skipping certain number of instances.

        Returns:
            An array of actions fetched for a queried page. Empty if the end was reached at the previous step.
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            response = await self._paginator.fetch_next_page(
                client, limit=limit, offset=offset
            )

            return [Action._from_engine_format(action) for action in response]

    async def reset_pagination(self):
        self._paginator = Paginator(ACTION_ENDPOINT)
