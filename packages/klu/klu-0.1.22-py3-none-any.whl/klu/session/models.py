"""
This module provides data models for the Session.
"""

from dataclasses import asdict, dataclass
from typing import Optional

from klu.common.models import BaseEngineModel


@dataclass
class Session(BaseEngineModel):
    """
    This class represents the Session data returned from the Klu engine
    """

    id: int
    guid: str
    action_id: int
    created_by_id: str
    extUserIds: Optional[str] = None
    name: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __repr__(self):
        return self.generate_repr()

    @classmethod
    def _from_engine_format(cls, data: dict) -> "Session":
        return cls._create_instance(
            **{
                "action_id": data.pop("actionId", None),
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

        base_dict.pop("action_id", None)
        base_dict.pop("updated_at", None)
        base_dict.pop("created_at", None)
        base_dict.pop("created_by_id", None)

        return base_dict
