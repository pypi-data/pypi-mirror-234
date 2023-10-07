""" This module provides data models for the Workspace. """
from dataclasses import asdict, dataclass

from klu.common.models import BaseEngineModel


@dataclass
class Workspace(BaseEngineModel):
    """
    This class represents the Workspace data model returned from the Klu engine
    """

    id: str
    name: str
    slug: str
    created_by_id: str
    """
        Workspace unique identifier. This is the id you can later use to query this object and create app.
    """
    project_guid: str

    def __repr__(self):
        return self.generate_repr()

    @classmethod
    def _from_engine_format(cls, data: dict) -> "Workspace":
        return cls._create_instance(
            **{
                "created_by_id": data.pop("createdById", None),
            },
            **data,
        )

    def _to_engine_format(self) -> dict:
        base_dict = asdict(self)

        return {
            "createdById": base_dict.pop("created_by_id", None),
            **base_dict,
        }
