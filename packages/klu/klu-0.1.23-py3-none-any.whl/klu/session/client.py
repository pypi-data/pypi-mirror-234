# mypy: disable-error-code="override"
from typing import NoReturn, Optional

from klu.common.client import KluClientBase
from klu.common.errors import NotSupportedError
from klu.session.constants import SESSION_ENDPOINT
from klu.session.models import Session


class SessionClient(KluClientBase):
    def __init__(self, api_key: str):
        super().__init__(api_key, SESSION_ENDPOINT, Session)

    async def create(
        self, action: str, name: Optional[str] = None, extUserId: Optional[str] = None
    ) -> Session:
        """
        Creates a session based on the data provided.

        Args:
            action_guid (str): Guid of the action object this session is attached to.
            name Optional[str]: Name of the session. If not provided will be left blank.

        Returns:
            A newly created Session object.
        """
        return await super().create(action=action, name=name, extUserId=extUserId)

    async def get(self, guid: str) -> Session:
        """
        Retrieves session information based on the unique Session guid, created during the Session creation.

        Args:
            guid (str): GUID of a session to fetch. The one that was used during the session creation

        Returns:
            Session object
        """
        return await super().get(guid)

    async def update(self) -> NoReturn:
        raise NotSupportedError()

    async def delete(self, guid: str) -> Session:
        """
        Delete session based on the id.

        Args:
            guid (str): Unique Guid of a session to delete.

        Returns:
            Deleted session object
        """
        return await super().delete(guid)
