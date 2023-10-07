"""
This module provides data models for the Model.
"""

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List, Optional

from klu.common.models import BaseEngineModel


@dataclass
class Model(BaseEngineModel):
    """
    This class represents the Model data returned from the Klu engine
    """

    guid: str
    llm: str
    provider: str
    provider_guid: str
    default: bool = False
    updated_at: Optional[str] = None
    created_at: Optional[str] = None
    created_by_id: Optional[str] = None

    def __repr__(self):
        return self.generate_repr()

    @classmethod
    def _from_engine_format(cls, data: dict) -> "Model":
        return cls._create_instance(
            **{
                "updated_at": data.pop("updatedAt", None),
                "created_at": data.pop("createdAt", None),
                "created_by_id": data.pop("createdById", None),
            },
            **data,
        )

    def _to_engine_format(self) -> dict:
        base_dict = asdict(
            self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )

        base_dict.pop("updated_at", None)
        base_dict.pop("created_at", None)
        base_dict.pop("created_by_id", None)

        return base_dict


@dataclass
class Provider(BaseEngineModel):
    """
    This class represents the Provider data returned from the Klu engine
    """

    guid: str
    name: str
    default: bool
    url: Optional[str] = None
    updated_at: Optional[str] = None
    created_at: Optional[str] = None
    created_by_id: Optional[str] = None

    def __repr__(self):
        return self.generate_repr()

    @classmethod
    def _from_engine_format(cls, data: dict) -> "Model":
        return cls._create_instance(
            **{
                "updated_at": data.pop("updatedAt", None),
                "created_at": data.pop("createdAt", None),
                "created_by_id": data.pop("createdById", None),
            },
            **data,
        )

    def _to_engine_format(self) -> dict:
        base_dict = asdict(
            self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )

        base_dict.pop("updated_at", None)
        base_dict.pop("created_at", None)
        base_dict.pop("created_by_id", None)

        return base_dict


@dataclass
class ProviderWithModels(BaseEngineModel):
    provider: Provider
    models: List[Model]
