# mypy: disable-error-code="override"
from typing import List, Optional

import aiohttp
from aiohttp import ClientResponseError

from klu.app.models import App
from klu.common.client import KluClientBase
from klu.common.errors import UnknownKluAPIError
from klu.context.models import Context
from klu.model.models import Model
from klu.utils.paginator import Paginator
from klu.workspace.constants import (
    DEFAULT_WORKSPACE_PAGE_SIZE,
    WORKSPACE_APPS_ENDPOINT,
    WORKSPACE_CONTEXTS_ENDPOINT,
    WORKSPACE_ENDPOINT,
    WORKSPACE_MODELS_ENDPOINT,
)
from klu.workspace.errors import WorkspaceOrUserNotFoundError
from klu.workspace.models import Workspace


class WorkspaceClient(KluClientBase):
    def __init__(self, api_key: str):
        super().__init__(api_key, WORKSPACE_ENDPOINT, Workspace)
        self._paginator = Paginator(WORKSPACE_ENDPOINT)

    async def create(self, name: str, slug: str) -> Workspace:
        """
        Creates a Workspace based on the data provided.

        Args:
            name (str): Model key. Required
            slug (str): Workspace slug. The unique name you would prefer to use to access the model.

        Returns:
            A newly created Workspace object.
        """
        return await super().create(name=name, slug=slug)

    async def get(self, guid: str) -> Workspace:
        """
        Retrieves a single workspace object by provided workspace id

        Args:
            guid (str): The ID of a workspace to fetch. project_guid you sent during the workspace creation

        Returns:
            A workspace object
        """
        return await super().get(guid)

    async def update(self, guid: str, name: str) -> Workspace:
        """
        Update workspace data. Currently, only name update is supported.

        Args:
            guid (str): ID of a context to update. project_guid you sent during the workspace creation
            name: str. New workspace name.

        Returns:
            Updated workspace instance
        """
        return await super().update(guid=guid, name=name)

    async def delete(self, guid: str) -> Workspace:
        """
        Delete Workspace based on the id.

        Args:
            guid (str): ID of a workspace to delete. project_guid you sent during the workspace creation

        Returns:
            Deleted workspace object
        """
        return await super().delete(guid)

    async def get_apps(self, guid: str) -> List[App]:
        """
        Retrieves the list of apps for workspace defined by provided guid

        Args:
            guid (str): The ID of workspace to fetch apps for.

        Returns:
            List of apps found in a workspace
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            try:
                response = await client.get(
                    WORKSPACE_APPS_ENDPOINT.format(id=guid),
                )
                return [App._from_engine_format(app) for app in response]
            except ClientResponseError as e:
                if e.status == 404:
                    raise WorkspaceOrUserNotFoundError()

                raise UnknownKluAPIError(e.status, e.message)

    async def get_contexts(self, guid: str) -> List[Context]:
        """
        Retrieves the list of contexts for workspace defined by provided guid

        Args:
            guid (str): The ID of workspace to fetch contexts for.
                project_guid you sent during the workspace creation

        Returns:
            List of Context objects found on a workspace.
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            try:
                response = await client.get(
                    WORKSPACE_CONTEXTS_ENDPOINT.format(id=guid),
                )
                return [Context._from_engine_format(context) for context in response]
            except ClientResponseError as e:
                if e.status == 404:
                    raise WorkspaceOrUserNotFoundError()

                raise UnknownKluAPIError(e.status, e.message)

    async def get_models(self, guid: str) -> List[Model]:
        """
        Retrieves the list of models for provided workspace id

        Args:
            guid (str): The ID of workspace to fetch models for. project_guid you sent during the workspace creation

        Returns:
            List of Model objects found on a workspace.
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            try:
                response = await client.get(
                    WORKSPACE_MODELS_ENDPOINT.format(id=guid),
                )
                return [Model._from_engine_format(model) for model in response]
            except ClientResponseError as e:
                if e.status == 404:
                    raise WorkspaceOrUserNotFoundError()

                raise UnknownKluAPIError(e.status, e.message)

    async def list(self) -> List[Workspace]:
        """
        Retrieves all workspaces for a user represented by the used API_KEY.
        Does not rely on internal paginator state, so `reset_pagination` method call can be skipped

        Returns:
            An array of all workspaces
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            response = await self._paginator.fetch_all(client)

            return [Workspace._from_engine_format(workspace) for workspace in response]

    async def fetch_single_page(
        self, page_number, limit: int = DEFAULT_WORKSPACE_PAGE_SIZE
    ) -> List[Workspace]:
        """
        Retrieves a single page of workspaces.
        Can be used to fetch a specific page of workspaces provided a certain per_page config.
        Does not rely on internal paginator state, so `reset_pagination` method call can be skipped

        Args:
            page_number (int): Number of the page to fetch
            limit (int): Number of instances to fetch per page. Defaults to 50

        Returns:
            An array of workspaces fetched for a queried page. Empty if queried page does not exist
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            response = await self._paginator.fetch_single_page(
                client, page_number, limit=limit
            )

            return [Workspace._from_engine_format(workspace) for workspace in response]

    async def fetch_next_page(
        self, limit: int = DEFAULT_WORKSPACE_PAGE_SIZE, offset: Optional[int] = None
    ) -> List[Workspace]:
        """
        Retrieves the next page of workspaces. Can be used to fetch a flexible number of pages starting.
        The place to start from can be controlled by the offset parameter.
        After using this method, we suggest to call `reset_pagination` method to reset the page cursor.

        Args:
            limit (int): Number of instances to fetch per page. Defaults to 50
            offset (int): The number of instances to skip. Can be used to query the pages of workspaces skipping certain number of instances.

        Returns:
            An array of workspaces fetched for a queried page. Empty if the end was reached at the previous step.
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)
            response = await self._paginator.fetch_next_page(
                client, limit=limit, offset=offset
            )

            return [Workspace._from_engine_format(workspace) for workspace in response]

    async def reset_pagination(self):
        self._paginator = Paginator(WORKSPACE_ENDPOINT)
