"""
This module provides data models for the Action.
"""
from dataclasses import asdict, dataclass
from typing import Any, AsyncIterator, Dict, Optional

from klu.api.sse_client import SSEClient
from klu.common.models import (
    BaseDataClass,
    BaseEngineModel,
    PromptInput,
    TaskStatusEnum,
)


@dataclass
class Action(BaseEngineModel):
    """
    This class represents the Action data model returned from the Klu engine
    """

    guid: str
    name: str
    app: str
    model: str
    action_type: str
    prompt: PromptInput
    system_message: Optional[str]
    description: Optional[str]
    model_config: Optional[dict]
    updated_at: Optional[str] = None
    created_at: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None

    def __repr__(self):
        return self.generate_repr()

    @classmethod
    def _from_engine_format(cls, data: dict) -> "Action":
        return cls._create_instance(
            **{
                "updated_at": data.pop("updatedAt", None),
                "created_at": data.pop("createdAt", None),
            },
            **data,
        )

    def _to_engine_format(self) -> dict:
        base_dict = asdict(self)

        return {
            "meta_data": base_dict.pop("meta_data", None),
            "updatedAt": base_dict.pop("updated_at", None),
            "createdAt": base_dict.pop("created_at", None),
            **base_dict,
        }


@dataclass
class PromptResponse(BaseDataClass):
    """
    This class represents the Response data model returned from the Klu engine in response to action prompting.
    """

    msg: str
    streaming: bool
    data_guid: Optional[str] = None
    result_url: Optional[str] = None
    feedback_url: Optional[str] = None
    streaming_url: Optional[str] = None

    def __repr__(self):
        return self.generate_repr()


@dataclass
class SyncPromptResponse(BaseDataClass):
    """
    This class represents the Response data model returned
    from the Klu engine in response to non-async, non-streaming action prompting.
    """

    msg: str
    data_guid: Optional[str] = None
    feedback_url: Optional[str] = None

    def __repr__(self):
        return self.generate_repr()


@dataclass
class StreamingPromptResponse(BaseDataClass):
    """
    This class represents the Response data model returned from the Klu engine in response to streaming action prompting.
    """

    msg: str
    streaming_url: Optional[str]
    data_guid: Optional[str] = None

    feedback_url: Optional[str] = None
    sse_client: Optional[SSEClient] = None

    @classmethod
    def _create_instance(cls, **kwargs):
        instance = cls.__new__(cls)
        instance._init_with_base_class(**kwargs)
        return instance

    def _init_with_base_class(self, **kwargs):
        super()._init_with_base_class(**kwargs)
        if self.streaming_url:
            self.sse_client = SSEClient(self.streaming_url)

    @property
    def tokens(self) -> Optional[AsyncIterator[str]]:
        return self.sse_client.get_streaming_data() if self.sse_client else None

    def __repr__(self):
        return self.generate_repr()


@dataclass
class AsyncPromptResponse(BaseDataClass):
    """
    This class represents the Response data model returned from the Klu engine in response to async action prompting.
    Contains result_url  - the url that gives access to the result when the prompt is completed or a message about prompting in progress.
    """

    msg: str
    data_guid: Optional[str] = None
    result_url: Optional[str] = None
    feedback_url: Optional[str] = None

    def __repr__(self):
        return self.generate_repr()


@dataclass
class AsyncPromptResultResponse(BaseDataClass):
    """
    This class represents the Response data model returned from the Klu engine in response to triggering result_url
    returned from the async prompting endpoint.
    msg will contain the result once the prompting task is completed.
    """

    msg: str
    status: TaskStatusEnum

    def __repr__(self):
        return self.generate_repr()
