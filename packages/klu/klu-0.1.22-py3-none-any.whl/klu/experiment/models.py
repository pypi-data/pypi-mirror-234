"""
This module provides data models for the Experiment.
"""

from dataclasses import asdict, dataclass
from typing import Optional

from klu.common.models import BaseEngineModel


@dataclass
class Experiment(BaseEngineModel):
    """
    This class represents the Experiment data returned from the Klu engine
    """

    guid: str
    name: str
    status: str
    app_guid: str
    action_primary_guid: str
    action_secondary_guid: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __repr__(self):
        return self.generate_repr()

    @classmethod
    def _from_engine_format(cls, data: dict) -> "Experiment":
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
