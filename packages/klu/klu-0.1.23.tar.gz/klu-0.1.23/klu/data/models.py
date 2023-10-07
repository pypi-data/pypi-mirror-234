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
class DataBaseClass(BaseEngineModel):
    """
    This class represents the generic data information that is stored in the Klu database
    """

    action: str
    input: str
    output: str
    session: Optional[str] = None
    metadata: Optional[dict] = None
    model: Optional[str] = None
    model_provider: Optional[str] = None
    full_prompt_sent: Optional[dict] = None
    system_message: Optional[str] = None
    latency: Optional[int] = None
    num_output_tokens: Optional[int] = None
    num_input_tokens: Optional[int] = None

    def __repr__(self):
        return self.generate_repr()

    @classmethod
    def _from_engine_format(cls, data: dict) -> "DataBaseClass":
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

        return base_dict


# We need this way of inheritance to append optional field after the required ones.
@dataclass
class Data(DataBaseClass, DataWithId):
    """
    This class represents the Data model returned from the Klu engine
    """

    @classmethod
    def _from_engine_format(cls, data: dict) -> "Data":
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

        return base_dict


@dataclass
class ActionData(DataBaseClass, DataWithFeedbackUrl):
    """
    This class represents the Data model returned from the Klu engine in response to Action data request
    """

    @classmethod
    def _from_engine_format(cls, data: dict) -> "ActionData":
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

        return base_dict


class DataSourceType(BasicStringEnum):
    """The enum used to represent the source of the Data"""

    SDK = "SDK"
    API = "API"
    BACK_FILL = "backfill"
