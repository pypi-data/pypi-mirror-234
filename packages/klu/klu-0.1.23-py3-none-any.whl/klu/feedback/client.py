# mypy: disable-error-code="override"
from typing import Optional

from klu.common.client import KluClientBase
from klu.feedback.constants import FEEDBACK_ENDPOINT
from klu.feedback.models import Feedback
from klu.utils.dict_helpers import dict_no_empty


class FeedbackClient(KluClientBase):
    def __init__(self, api_key: str):
        super().__init__(api_key, FEEDBACK_ENDPOINT, Feedback)

    async def create(
        self,
        type: str,
        value: str,
        data_guid: int,
        created_by: str,
        metadata: Optional[dict] = None,
        source: str = 'api',
    ) -> Feedback:
        """
        Creates new feedback on a data point.

        Args:
            type (str): Type of feedback
            value (str): Value of feedback
            data_guid (int): ID of a data point to create feedback on
            created_by (str): User who created the feedback
            meta_data (dict): Metadata of feedback
            source (str): Source of feedback

        Returns:
            Created Feedback object
        """
        return await super().create(
            type=type,
            value=value,
            data=data_guid,
            createdById=created_by,
            source=source,
            meta_data=metadata,
        )

    async def get(self, guid: str) -> Feedback:
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
        type: Optional[str] = None,
        value: Optional[str] = None,
        source: Optional[str] = None,
        created_by: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> Feedback:
        """
        Update feedback information.

        Args:
            guid (str): ID of a feedback object to update.
            type (str): Type of feedback
            value (str): Value of feedback
            source (str): Source of feedback
            created_by (str): User who created the feedback
            metadata (dict): Metadata of feedback

        Returns:
            Newly updated Feedback object
        """
        data = {
            "type": type,
            "value": value,
            "source": source,
            "created_by": created_by,
            "metadata": metadata,
        }
        return await super().update(**{"guid": guid, **dict_no_empty(data)})

    async def delete(self, guid: str) -> Feedback:
        return await super().delete(guid)
