from abc import ABCMeta, abstractmethod
from dataclasses import MISSING, dataclass, fields
from enum import Enum
from typing import Any, Dict, Optional, Union


class BasicEnum(Enum):
    """
    Basic class for enums across the projects. Adds basic functions to list names and values.
    Overrides comparison function to allow comparing against string values.
    """

    __hash__ = Enum.__hash__

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other.upper()
        return super().__eq__(other)

    @classmethod
    def list_values(cls) -> list:
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list_names(cls) -> list:
        return list(map(lambda c: c.name, cls))


class BasicStringEnum(str, BasicEnum):
    """
    Basic class for string-based enums across the projects.
    Allows to have human-readable representation of enum as a value and convert between such value and key.
    """

    def __str__(self):
        return self.value

    @classmethod
    def get(cls, member: str) -> Optional["BasicStringEnum"]:
        """
        Get a member of an Enum by its string representation
        """
        member = member.upper().replace(" ", "_")
        try:
            return cls.__members__[member]
        except KeyError:
            return None

    def get_human_string(self):
        return self.value.replace("_", " ").capitalize() if self.value else None


@dataclass
class BaseDataClass:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    """
        This is the function that helps us to create an object in a way that any unknown kwargs passed will be ignored
    """

    @classmethod
    def _create_instance(cls, **kwargs):
        instance = cls.__new__(cls)
        instance._init_with_base_class(**kwargs)
        return instance

    def _init_with_base_class(self, **kwargs):
        for field_obj in fields(self):
            if field_obj.name in kwargs:
                value = kwargs[field_obj.name]
            elif field_obj.default is not MISSING:
                value = field_obj.default
            elif field_obj.default_factory is not MISSING:
                value = field_obj.default_factory()
            else:
                # TODO consider adding sentry log here to spot
                #  missing data from engine response (reflecting models discrepancy) in advance.
                # logging.warning(
                #     f"Missing required field {field_obj.name}. The field has been set to None by default. "
                #     "If you are unsure why this field is missing, please contact our team."
                # )
                value = None
            setattr(self, field_obj.name, value)

    def generate_repr(self):
        repr_str = f"{self.__class__.__name__}("
        for field in fields(self):
            field_value = getattr(self, field.name, "undefined")
            repr_str += f"{field.name}={field_value}, "
        repr_str = repr_str.rstrip(", ")
        repr_str += ")"
        return repr_str


class BaseEngineModel(BaseDataClass, metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def _from_engine_format(cls, data: dict) -> "BaseEngineModel":
        pass

    @abstractmethod
    def _to_engine_format(self) -> dict:
        pass


class TaskStatusEnum(BasicStringEnum):
    """The enum used to represent the status of any processing task status. Based on celery statuses."""

    # The task is waiting for execution.
    PENDING = "PENDING"
    # The task has been started.
    STARTED = "STARTED"

    # The task is to be retried, possibly because of failure.
    RETRY = "RETRY"
    # The task raised an exception, or has exceeded the retry limit.
    FAILURE = "FAILURE"
    # The task executed successfully.
    SUCCESS = "SUCCESS"


"""
This type defines input that can be sent to a prompt.
It can either be a string or a Dict with properties you defined in Klu
"""
PromptInput = Union[str, Dict[str, Any]]
