"""
This module provides data models for the Data.
"""

from abc import ABC
from dataclasses import asdict, dataclass
from typing import Optional

from klu.common.models import BaseEngineModel, BasicStringEnum


@dataclass
class DataWithId(BaseEngineModel, ABC):
    """
    This class represents the base data with Id after it has been persisted into the Klu Database
    """

    guid: str

    def __repr__(self):
        return self.generate_repr()


@dataclass
class DataWithFeedbackUrl(BaseEngineModel, ABC):
    """
    This class represents the data specific to the model returned from the Action prompting
    """

    feedback_url: int

    def __repr__(self):
        return self.generate_repr()


@dataclass
class Feedback(BaseEngineModel):
    """
    This class represents the generic data information that is stored in the Klu database
    """

    guid: str
    type: str = ""
    value: str = ""
    data_guid: str = ""
    source: str = ""
    created_by: str = ""
    deleted: bool = False
    metadata: Optional[dict] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __repr__(self):
        return self.generate_repr()

    @classmethod
    def _from_engine_format(cls, data: dict) -> "Feedback":
        data["created_by"] = data.pop("createdById", None)
        data["data"] = data.pop("data_guid", None)
        data["metadata"] = data.pop("meta_data", None)
        return cls._create_instance(
            **{
                "updated_at": data.pop("updatedAt", None),
                "created_at": data.pop("createdAt", None),
            },
            **data,
        )

    def _to_engine_format(self) -> dict:
        base_dict = asdict(
            self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )

        base_dict.pop("updated_at", None)
        base_dict.pop("created_at", None)
        base_dict["createdById"] = base_dict.pop("created_by", None)
        base_dict["data"] = base_dict.pop("data_guid", None)
        base_dict["meta_data"] = base_dict.pop("metadata", None)
        print(base_dict)
        return base_dict
